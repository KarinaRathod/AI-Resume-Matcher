import os
from dotenv import load_dotenv
import streamlit as st
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
import re

from crewai import Agent, Task, Crew, LLM

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()

# -----------------------------
# GEMINI LLM
# -----------------------------
llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# -----------------------------
# STREAMLIT CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Matcher PRO", layout="wide")
st.title("💼 AI Resume Matcher PRO")
st.caption("Analyze, score, and improve your resume with AI")

# -----------------------------
# PDF READER FUNCTION
# -----------------------------
def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text

# -----------------------------
# INPUT
# -----------------------------
st.subheader("📄 Upload Resume")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

resume_text = ""
if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ Resume uploaded successfully!")

st.subheader("📋 Job Description")
job_desc = st.text_area("Paste Job Description:", height=200)

# -----------------------------
# BUTTON
# -----------------------------
if st.button("🚀 Analyze Resume", use_container_width=True):

    if not resume_text or not job_desc.strip():
        st.warning("⚠️ Upload resume and enter job description")
        st.stop()

    with st.spinner("🧠 Running AI analysis..."):

        # -----------------------------
        # AGENTS
        # -----------------------------
        analyzer = Agent(
            role="Resume Analyzer",
            goal="Extract structured info from resume",
            backstory="Expert HR recruiter",
            llm=llm
        )

        matcher = Agent(
            role="ATS Matcher",
            goal="Calculate match score",
            backstory="ATS system expert",
            llm=llm
        )

        advisor = Agent(
            role="Career Coach",
            goal="Suggest improvements",
            backstory="Helps candidates get hired",
            llm=llm
        )

        rewriter = Agent(
            role="Resume Writer",
            goal="Rewrite resume to improve ATS score",
            backstory="Professional resume writer",
            llm=llm
        )

        # -----------------------------
        # TASKS (FIXED ✅)
        # -----------------------------
        analysis_task = Task(
            description=f"""
            Analyze resume:

            {resume_text}

            Extract:
            - Skills
            - Experience
            - Projects
            """,
            expected_output="""
            Structured analysis:
            - Skills list
            - Experience summary
            - Key strengths
            """,
            agent=analyzer
        )

        match_task = Task(
            description=f"""
            Compare resume with job description:

            JOB:
            {job_desc}

            Provide:
            - Match Score (0-100)
            - Matching skills
            - Missing skills
            """,
            expected_output="""
            - Match percentage
            - Matching skills
            - Missing skills
            """,
            agent=matcher
        )

        advice_task = Task(
            description="""
            Give actionable suggestions to improve resume.
            """,
            expected_output="""
            Bullet points with improvement suggestions
            """,
            agent=advisor
        )

        rewrite_task = Task(
            description="""
            Rewrite the resume to better match the job.
            """,
            expected_output="""
            Improved and optimized resume
            """,
            agent=rewriter
        )

        # -----------------------------
        # CREW
        # -----------------------------
        crew = Crew(
            agents=[analyzer, matcher, advisor, rewriter],
            tasks=[analysis_task, match_task, advice_task, rewrite_task],
            verbose=False
        )

        result = crew.kickoff()
        output = result.raw.strip()  # ✅ FIXED

    # -----------------------------
    # DISPLAY OUTPUT
    # -----------------------------
    st.success("✅ Analysis Complete!")

    # -----------------------------
    # MATCH SCORE (safe extraction)
    # -----------------------------
    score = 70  # fallback
    match = re.search(r'\b(100|\d{1,2})\b', output)
    if match:
        score = int(match.group(0))

    st.subheader("📊 Match Score")
    st.progress(score / 100)
    st.write(f"### {score}% Match")

    # -----------------------------
    # TABS
    # -----------------------------
    tab1, tab2, tab3 = st.tabs(["📊 Full Report", "💡 Improvements", "✍️ Rewrite"])

    with tab1:
        st.markdown(output)

    with tab2:
        st.markdown("""
        ✔ Add keywords from job description  
        ✔ Quantify achievements (numbers, % growth)  
        ✔ Highlight relevant projects  
        ✔ Keep formatting ATS-friendly  
        """)

    with tab3:
        st.info("Rewritten resume is included in the report above.")

    # -----------------------------
    # PIE CHART
    # -----------------------------
    st.subheader("📉 Skill Gap Analysis")

    labels = ["Match", "Gap"]
    values = [score, 100 - score]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%")
    ax.set_title("Skill Match vs Gap")

    st.pyplot(fig)

    # -----------------------------
    # DOWNLOAD
    # -----------------------------
    st.download_button(
        "⬇️ Download Report",
        data=output,
        file_name="resume_analysis.txt",
        mime="text/plain"
    )
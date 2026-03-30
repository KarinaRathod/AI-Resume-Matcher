
# 💼 AI Resume Matcher (CrewAI + Gemini)

An advanced multi-agent AI system that analyzes resumes against job descriptions, calculates match scores, identifies skill gaps, and suggests improvements — all through an interactive Streamlit dashboard.

---

## 🚀 Features

- 🧠 Multi-Agent System (CrewAI)
  - Resume Analyzer → extracts skills & experience
  - ATS Matcher → calculates match score
  - Career Advisor → suggests improvements
  - Resume Writer → rewrites resume for better match

- 📄 PDF Resume Upload Support
- 📊 Match Score Visualization (progress bar + pie chart)
- 🎯 Skill Gap Analysis
- ✍️ AI Resume Rewriting
- 📥 Downloadable Report

---

## 🛠️ Tech Stack

- Python
- CrewAI
- Google Gemini (via CrewAI LLM)
- Streamlit
- PyPDF2
- Matplotlib

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ai-resume-matcher.git
cd ai-resume-matcher
````

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Setup Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

Get API key:
👉 [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

---

### 4️⃣ Run the App

```bash
streamlit run app.py
```

---

## 🧪 How to Use

1. Upload your resume (PDF)
2. Paste a job description
3. Click **Analyze Resume**
4. View:

   * Match score 📊
   * Skill gaps 📉
   * Suggestions 💡
   * Rewritten resume ✍️
5. Download full report

---

## 📊 Output Includes

* Resume analysis (skills, experience)
* Match percentage (ATS-style)
* Matching vs missing skills
* Actionable improvement suggestions
* AI-enhanced rewritten resume
* Visual skill gap chart

---


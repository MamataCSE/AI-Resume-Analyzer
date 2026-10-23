import streamlit as st
import re
from datetime import datetime

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write(
    "Analyze your resume, compare job requirements, "
    "and discover skills to improve."
)

st.divider()

resume = st.file_uploader(
    "📤 Upload your resume",
    type=["pdf", "txt"]
)

job_description = st.text_area(
    "💼 Job description",
    placeholder="Paste the job requirements here..."
)

if resume is not None:
    st.success(f"Uploaded: {resume.name}")

    if st.button("🔍 Analyze Resume", type="primary"):
        try:
            if resume.name.lower().endswith(".txt"):
                text = resume.getvalue().decode(
                    "utf-8", errors="ignore"
                )
            else:
                import pypdf
                reader = pypdf.PdfReader(resume)
                text = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )

        except Exception as error:
            st.error(f"Could not read resume: {error}")
            st.stop()

        if not text.strip():
            st.error(
                "No readable text found. Try a text-based PDF "
                "or a TXT file."
            )
            st.stop()

        words = re.findall(r"\b[a-zA-Z+#.]+\b", text.lower())
        word_count = len(words)

        skills = [
            "python", "java", "c++", "html", "css",
            "javascript", "sql", "machine learning",
            "data analysis", "communication", "teamwork",
            "git", "react", "excel", "problem-solving",
            "streamlit", "flask", "django", "mongodb",
            "power bi"
        ]

        resume_lower = text.lower()

        found_skills = [
            skill for skill in skills
            if skill in resume_lower
        ]

        job_words = set(
            re.findall(
                r"\b[a-zA-Z+#.]{2,}\b",
                job_description.lower()
            )
        )

        resume_words = set(words)

        matched = sorted(job_words & resume_words)
        missing = sorted(job_words - resume_words)

        score = (
            round(len(matched) / len(job_words) * 100)
            if job_words else None
        )

        st.divider()
        st.header("📊 Resume Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Words", word_count)

        with col2:
            st.metric("Skills Detected", len(found_skills))

        with col3:
            st.metric(
                "Keyword Match",
                f"{score}%" if score is not None else "N/A"
            )

        if score is not None:
            st.subheader("🎯 Job Match Score")
            st.progress(score / 100)
            st.caption(
                "This is a basic keyword-overlap score, "
                "not a professional ATS score."
            )
        else:
            st.info(
                "Add a job description to calculate the "
                "keyword match score."
            )

        left, right = st.columns(2)

        with left:
            st.subheader("✅ Matching Keywords")
            st.write(", ".join(matched) or "No matches found.")

        with right:
            st.subheader("💡 Keywords to Consider")
            st.write(
                ", ".join(missing)
                if job_description.strip()
                else "Enter a job description to compare."
            )

        st.divider()
        st.header("📈 Skills Dashboard")

        if found_skills:
            st.bar_chart({
                "Detected": [1] * len(found_skills)
            }, height=250)

            st.write("**Your detected skills:**")
            st.write(" • ".join(found_skills))
        else:
            st.warning(
                "No predefined skills detected. "
                "Check the resume text or add relevant skills."
            )

        st.header("📝 Improvement Suggestions")

        suggestions = []

        if word_count < 100:
            suggestions.append(
                "Add more relevant details about your education, "
                "projects, and skills."
            )

        if not found_skills:
            suggestions.append(
                "Include relevant technical and soft skills."
            )

        if "project" not in resume_lower:
            suggestions.append(
                "Add a Projects section describing your work."
            )

        if "education" not in resume_lower:
            suggestions.append(
                "Include your Education section."
            )

        if "experience" not in resume_lower:
            suggestions.append(
                "Include relevant experience or internships, "
                "if applicable."
            )

        if missing and job_description.strip():
            suggestions.append(
                "Review the missing job keywords and include "
                "relevant ones only if they accurately describe "
                "your skills."
            )

        if suggestions:
            for item in suggestions:
                st.write("•", item)
        else:
            st.success(
                "Your resume includes several useful sections. "
                "Review it for accuracy and clarity."
            )

        st.divider()
        st.header("📥 Download Analysis Report")

        report = f"""
AI RESUME ANALYZER - ANALYSIS REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

Resume file: {resume.name}
Total words: {word_count}
Detected skills: {", ".join(found_skills) or "None"}

Keyword match: {str(score) + "%" if score is not None else "Not calculated"}

Matching keywords:
{", ".join(matched) or "None"}

Keywords to consider:
{", ".join(missing) if job_description.strip() else "No job description provided"}

Improvement suggestions:
{chr(10).join("- " + item for item in suggestions) or "Review resume for clarity."}

Note: This is a basic keyword comparison, not an AI hiring
decision or a professional ATS score.
"""

        st.download_button(
            label="⬇️ Download Report",
            data=report,
            file_name="resume_analysis_report.txt",
            mime="text/plain"
        )

        with st.expander("📃 View Extracted Resume Text"):
            st.text(text)

        st.success("Resume analysis completed!")

else:
    st.info("Upload a PDF or TXT resume to get started.")
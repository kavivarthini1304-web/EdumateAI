import streamlit as st
import google.generativeai as genai
import os
import PyPDF2
from docx import Document
import tempfile

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="EduMate AI",
    page_icon="📚",
    layout="wide"
)

# -------------------------------
# Gemini API Configuration
# -------------------------------
API_KEY = "AQ.Ab8RN6JYeVZOo54eqiTBH-BivJaQtpw9RLrv79x-W7_Ey5LaYA"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------------
# Custom CSS
# -------------------------------
st.markdown("""
<style>
.main-title{
    text-align:center;
    color:#4CAF50;
    font-size:40px;
    font-weight:bold;
}
.feature-box{
    background-color:#f5f5f5;
    padding:15px;
    border-radius:10px;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📚 EduMate AI</h1>", unsafe_allow_html=True)
st.write("### Your Personal AI Study Assistant")

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("Navigation")

option = st.sidebar.radio(
    "Choose Feature",
    [
        "Home",
        "AI Summary",
        "Question Generator",
        "Quiz",
        "AI Chatbot"
    ]
)

# -------------------------------
# Home Page
# -------------------------------
if option == "Home":

    st.header("Welcome to EduMate AI")

    st.info(
        "Upload your study material and let AI help you learn faster."
    )

    uploaded_file = st.file_uploader(
        "Upload PDF / DOCX / TXT",
        type=["pdf", "docx", "txt"]
    )

    text = ""

    if uploaded_file is not None:

        file_type = uploaded_file.name.split(".")[-1]

        if file_type == "pdf":

            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            for page in pdf_reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        elif file_type == "docx":

            doc = Document(uploaded_file)

            for para in doc.paragraphs:
                text += para.text + "\n"

        elif file_type == "txt":

            text = uploaded_file.read().decode("utf-8")

        st.success("File Uploaded Successfully ✅")

        st.session_state["study_text"] = text

        st.subheader("Preview")

        st.write(text[:1000])
# ------------------------------------
# Gemini Helper Function
# ------------------------------------

def ask_gemini(prompt):

    try:

        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text

        return "No response generated."

    except Exception as e:

        return f"Error : {e}"


# ------------------------------------
# AI SUMMARY PAGE
# ------------------------------------

if option == "AI Summary":

    st.header("📖 AI Study Summary")

    if "study_text" not in st.session_state:

        st.warning("Please upload a study material from the Home page.")

    else:

        study_text = st.session_state["study_text"]

        st.success("Study Material Loaded Successfully")

        st.text_area(
            "Uploaded Text Preview",
            study_text[:2500],
            height=250
        )

        summary_type = st.selectbox(

            "Choose Summary Type",

            [
                "Short Summary",
                "Detailed Summary",
                "Bullet Points",
                "Important Concepts"
            ]

        )

        if st.button("Generate Summary"):

            with st.spinner("Generating Summary..."):

                if summary_type == "Short Summary":

                    prompt = f"""
Summarize the following study material in simple English within 200 words.

Text:
{study_text}
"""

                elif summary_type == "Detailed Summary":

                    prompt = f"""
Explain the following study material in detail with headings.

Text:
{study_text}
"""

                elif summary_type == "Bullet Points":

                    prompt = f"""
Convert this study material into important bullet points.

Text:
{study_text}
"""

                else:

                    prompt = f"""
Find the important concepts from this study material.
Explain each concept in simple language.

Text:
{study_text}
"""

                result = ask_gemini(prompt)

                st.subheader("📚 AI Result")

                st.write(result)

                st.download_button(

                    label="⬇ Download Summary",

                    data=result,

                    file_name="summary.txt",

                    mime="text/plain"

                )
# ------------------------------------
# QUESTION GENERATOR PAGE
# ------------------------------------

if option == "Question Generator":

    st.header("❓ AI Question Generator")

    if "study_text" not in st.session_state:

        st.warning("Please upload your study material first.")

    else:

        study_text = st.session_state["study_text"]

        question_type = st.selectbox(

            "Select Question Type",

            [
                "5 Questions",
                "10 Questions",
                "20 Questions",
                "Important Viva Questions",
                "MCQ Questions"
            ]

        )

        if st.button("Generate Questions"):

            with st.spinner("Generating Questions..."):

                if question_type == "5 Questions":

                    prompt = f"""
Generate 5 important questions from the following study material.

Text:
{study_text}
"""

                elif question_type == "10 Questions":

                    prompt = f"""
Generate 10 important questions from the following study material.

Text:
{study_text}
"""

                elif question_type == "20 Questions":

                    prompt = f"""
Generate 20 important questions from the following study material.

Text:
{study_text}
"""

                elif question_type == "Important Viva Questions":

                    prompt = f"""
Generate important viva questions with answers from the following study material.

Text:
{study_text}
"""

                else:

                    prompt = f"""
Generate 10 MCQ questions with four options and correct answers.

Text:
{study_text}
"""

                result = ask_gemini(prompt)

                st.subheader("Generated Questions")

                st.write(result)

                st.download_button(

                    label="⬇ Download Questions",

                    data=result,

                    file_name="questions.txt",

                    mime="text/plain"

                )
# ------------------------------------
# QUIZ PAGE
# ------------------------------------

if option == "Quiz":

    st.header("📝 AI Quiz Generator")

    if "study_text" not in st.session_state:

        st.warning("Please upload your study material first.")

    else:

        study_text = st.session_state["study_text"]

        if st.button("Create Quiz"):

            with st.spinner("Generating Quiz..."):

                prompt = f"""
Generate 5 multiple choice questions.

Rules:

1. Each question should have 4 options.
2. Mention the correct answer.
3. Give a short explanation.
4. Questions should be based only on the study material.

Study Material:

{study_text}
"""

                quiz = ask_gemini(prompt)

                st.subheader("📚 Generated Quiz")

                st.write(quiz)

                st.download_button(
                    "⬇ Download Quiz",
                    quiz,
                    "quiz.txt",
                    "text/plain"
                )

        st.divider()

        st.subheader("📊 Quick Self Assessment")

        q1 = st.radio(
            "Did you understand today's topic?",
            ["Yes", "Partially", "No"],
            key="q1"
        )

        q2 = st.radio(
            "Can you answer questions without notes?",
            ["Yes", "No"],
            key="q2"
        )

        q3 = st.radio(
            "Need AI Revision?",
            ["Yes", "No"],
            key="q3"
        )

        if st.button("Show Result"):

            score = 0

            if q1 == "Yes":
                score += 1

            if q2 == "Yes":
                score += 1

            if q3 == "No":
                score += 1

            st.success(f"Your Study Score : {score}/3")

            if score == 3:

                st.balloons()

                st.success("Excellent! Keep Learning 🚀")

            elif score == 2:

                st.info("Good Job! Revise once again.")

            else:

                st.warning("Need More Practice.")
                # ------------------------------------
# AI CHATBOT PAGE
# ------------------------------------

if option == "AI Chatbot":

    st.header("💬 EduMate AI Chatbot")

    st.write("Ask any study-related question.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input(
        "Enter your Question",
        key="chat_question"
    )

    if st.button("Ask AI"):

        if user_question.strip() == "":
            st.warning("Please enter a question.")

        else:

            with st.spinner("Thinking..."):

                prompt = f"""
You are an intelligent study assistant.

Answer the student's question in simple English.

Question:
{user_question}
"""

                answer = ask_gemini(prompt)

                st.session_state.chat_history.append(
                    ("You", user_question)
                )

                st.session_state.chat_history.append(
                    ("EduMate AI", answer)
                )

    if st.session_state.chat_history:

        st.subheader("Conversation")

        for sender, message in st.session_state.chat_history:

            if sender == "You":

                st.markdown(
                    f"**🧑 You:** {message}"
                )

            else:

                st.markdown(
                    f"**🤖 EduMate AI:** {message}"
                )

        if st.button("Clear Chat"):

            st.session_state.chat_history = []

            st.rerun()
# ------------------------------------
# AI STUDY TOOLS
# ------------------------------------

st.divider()

st.sidebar.header("📌 Quick Study Tools")

tool = st.sidebar.selectbox(
    "Choose Tool",
    [
        "None",
        "Study Tips",
        "Important Topics",
        "Exam Preparation",
        "Motivation"
    ]
)

if tool != "None":

    if st.button("Generate"):

        with st.spinner("Generating..."):

            if "study_text" in st.session_state:

                study_text = st.session_state["study_text"]

            else:

                study_text = ""

            if tool == "Study Tips":

                prompt = f"""
Give 10 effective study tips based on the following topic.

Topic:

{study_text}
"""

            elif tool == "Important Topics":

                prompt = f"""
Identify the most important topics from the following study material.

Text:

{study_text}
"""

            elif tool == "Exam Preparation":

                prompt = f"""
Create a one-day exam preparation plan using the following study material.

Text:

{study_text}
"""

            else:

                prompt = """
Give an inspirational motivational message for a college student preparing for exams.
"""

            result = ask_gemini(prompt)

            st.subheader(tool)

            st.write(result)

            st.download_button(

                "⬇ Download",

                result,

                file_name=f"{tool}.txt",

                mime="text/plain"

            )

# ------------------------------------
# FOOTER
# ------------------------------------

st.markdown("---")

st.markdown(
"""
<center>

### 📚 EduMate AI

AI Powered Smart Study Assistant

Made using ❤️ Streamlit + Google Gemini

</center>
""",
unsafe_allow_html=True
)
# ------------------------------------
# AI FLASH CARDS
# ------------------------------------

st.divider()

st.header("🧠 AI Flash Cards")

if "study_text" in st.session_state:

    if st.button("Generate Flash Cards"):

        with st.spinner("Creating Flash Cards..."):

            prompt = f"""
Create 15 flash cards.

Format:

Question :
Answer :

Study Material:

{st.session_state['study_text']}
"""

            flashcards = ask_gemini(prompt)

            st.write(flashcards)

            st.download_button(
                "⬇ Download Flash Cards",
                flashcards,
                "flashcards.txt",
                "text/plain"
            )

# ------------------------------------
# WORD COUNT
# ------------------------------------

if "study_text" in st.session_state:

    total_words = len(st.session_state["study_text"].split())

    st.sidebar.markdown("### 📊 Statistics")

    st.sidebar.metric(
        "Total Words",
        total_words
    )

    reading_time = max(1, total_words // 200)

    st.sidebar.metric(
        "Reading Time",
        f"{reading_time} min"
    )

# ------------------------------------
# STUDY PROGRESS
# ------------------------------------

st.sidebar.markdown("### 📈 Study Progress")

progress = st.sidebar.slider(
    "Completed",
    0,
    100,
    50
)

st.sidebar.progress(progress)

# ------------------------------------
# SESSION DETAILS
# ------------------------------------

if "study_text" in st.session_state:

    st.sidebar.success("Study Material Loaded")

else:

    st.sidebar.warning("Upload a File")

# ------------------------------------
# END
# ------------------------------------
# ------------------------------------
# AI NOTES GENERATOR
# ------------------------------------

st.divider()

st.header("📝 AI Notes Generator")

if "study_text" in st.session_state:

    note_type = st.selectbox(
        "Select Notes Format",
        [
            "Short Notes",
            "Exam Notes",
            "One Page Revision",
            "Important Definitions"
        ]
    )

    if st.button("Generate Notes"):

        with st.spinner("Generating Notes..."):

            if note_type == "Short Notes":

                prompt = f"""
Create short notes from the following study material.

Text:

{st.session_state['study_text']}
"""

            elif note_type == "Exam Notes":

                prompt = f"""
Prepare exam notes with headings and important points.

Text:

{st.session_state['study_text']}
"""

            elif note_type == "One Page Revision":

                prompt = f"""
Convert this study material into one-page revision notes.

Text:

{st.session_state['study_text']}
"""

            else:

                prompt = f"""
Extract important definitions from the study material.

Text:

{st.session_state['study_text']}
"""

            notes = ask_gemini(prompt)

            st.subheader("Generated Notes")

            st.write(notes)

            st.download_button(
                "⬇ Download Notes",
                notes,
                "notes.txt",
                "text/plain"
            )

# ------------------------------------
# TRANSLATOR
# ------------------------------------

st.divider()

st.header("🌍 Translate Notes")

language = st.selectbox(
    "Select Language",
    [
        "Tamil",
        "English",
        "Hindi"
    ]
)

if st.button("Translate"):

    if "study_text" in st.session_state:

        prompt = f"""
Translate the following study material into {language}.

Text:

{st.session_state['study_text']}
"""

        translated = ask_gemini(prompt)

        st.subheader("Translated Notes")

        st.write(translated)

        st.download_button(
            "⬇ Download Translation",
            translated,
            "translation.txt",
            "text/plain"
        )
# ------------------------------------
# BOOKMARK NOTES
# ------------------------------------

st.divider()

st.header("⭐ Bookmark Important Notes")

if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

bookmark_text = st.text_area(
    "Write important notes here"
)

if st.button("Save Bookmark"):

    if bookmark_text.strip():

        st.session_state.bookmarks.append(
            bookmark_text
        )

        st.success("Bookmark Saved Successfully")

if st.session_state.bookmarks:

    st.subheader("Saved Bookmarks")

    for i, note in enumerate(
        st.session_state.bookmarks
    ):

        st.markdown(
            f"**{i+1}.** {note}"
        )

# ------------------------------------
# FAVORITE QUESTIONS
# ------------------------------------

st.divider()

st.header("❤️ Favorite Questions")

favorite = st.text_area(
    "Paste your favorite question"
)

if st.button("Save Favorite"):

    if favorite.strip():

        if "favorite_questions" not in st.session_state:

            st.session_state.favorite_questions = []

        st.session_state.favorite_questions.append(
            favorite
        )

        st.success("Saved Successfully")

if "favorite_questions" in st.session_state:

    st.subheader("Favorite Questions")

    for i, q in enumerate(
        st.session_state.favorite_questions
    ):

        st.write(f"{i+1}. {q}")

# ------------------------------------
# STUDY REMINDER
# ------------------------------------

st.divider()

st.header("⏰ Study Reminder")

study_time = st.time_input(
    "Select Study Time"
)

study_goal = st.text_input(
    "Today's Goal"
)

if st.button("Save Reminder"):

    st.success(
        f"Reminder Saved for {study_time}"
    )

    st.info(
        f"Goal : {study_goal}"
    )

# ------------------------------------
# ABOUT PROJECT
# ------------------------------------

st.divider()

st.header("ℹ About EduMate AI")

st.write("""
EduMate AI is an AI Powered Study Assistant.

Features

✔ AI Summary

✔ AI Notes

✔ AI Chatbot

✔ Flash Cards

✔ Quiz Generator

✔ Question Generator

✔ Translator

✔ Exam Planner

✔ Bookmarks

✔ Study Reminder

Developed using

• Streamlit

• Python

• Google Gemini API
""")

                st.warning("Need More Practice.")
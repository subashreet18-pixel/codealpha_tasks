import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="FAQ Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.chat-title {
    text-align: center;
    font-size: 35px;
    font-weight: bold;
    color: #1f4e79;
    margin-bottom: 20px;
}

.user-message {
    background-color: #DCF8C6;
    padding: 12px;
    border-radius: 10px;
    margin: 8px 0;
    text-align: right;
    color: black;
}

.bot-message {
    background-color: #FFFFFF;
    padding: 12px;
    border-radius: 10px;
    margin: 8px 0;
    border-left: 5px solid #1f77b4;
    color: black;
}

.stDownloadButton button {
    width: 100%;
}

.sidebar-title {
    font-size: 22px;
    font-weight: bold;
    color: #1f77b4;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# FAQ DATASET
# ==========================================
faq_data = {
    "Question": [
        "What is CodeAlpha?",
        "How can I apply for an internship?",
        "Do internships provide certificates?",
        "What programming languages should I learn?",
        "How long is the internship?",
        "Is the internship free?",
        "How do I submit my projects?",
        "Can beginners apply?",
        "What is Python?",
        "What is Streamlit?"
    ],
    "Answer": [
        "CodeAlpha is a platform that provides internship opportunities and project-based learning experiences.",
        "You can apply through the official CodeAlpha website and complete the registration process.",
        "Yes, certificates are provided after successful completion of internship tasks.",
        "Popular languages include Python, Java, JavaScript, and C++.",
        "The internship duration may vary depending on the program offered.",
        "Most CodeAlpha internships are free to join. Check official announcements for details.",
        "Projects are usually submitted through the internship dashboard or provided submission links.",
        "Yes, beginners are encouraged to apply and learn through practical projects.",
        "Python is a high-level programming language widely used for AI, web development, automation, and data science.",
        "Streamlit is a Python framework used to build interactive web applications for machine learning and data science projects."
    ]
}

faq_df = pd.DataFrame(faq_data)

# ==========================================
# TF-IDF MODEL
# ==========================================
vectorizer = TfidfVectorizer()

faq_vectors = vectorizer.fit_transform(faq_df["Question"])

# ==========================================
# SESSION STATE
# ==========================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# FUNCTION TO FIND BEST ANSWER
# ==========================================
def get_best_answer(user_query):
    try:
        query_vector = vectorizer.transform([user_query])

        similarities = cosine_similarity(
            query_vector,
            faq_vectors
        )

        best_match_index = similarities.argmax()
        best_score = similarities[0][best_match_index]

        threshold = 0.25

        if best_score >= threshold:
            return faq_df.iloc[best_match_index]["Answer"]

        return (
            "Sorry, I couldn't find a relevant answer. "
            "Please try rephrasing your question."
        )

    except Exception as e:
        return f"An error occurred: {str(e)}"

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">📌 Project Information</div>',
        unsafe_allow_html=True
    )

    st.write("### FAQ Chatbot")
    st.write("""
    **Technology Used**
    - Python
    - Streamlit
    - TF-IDF
    - Cosine Similarity
    - Scikit-learn

    **Features**
    - Intelligent FAQ Matching
    - Chat Interface
    - Chat History
    - Download Conversation
    - Error Handling
    """)

    st.write("---")

    st.info(
        "This project is developed for the "
        "CodeAlpha AI Internship Program."
    )

# ==========================================
# TITLE
# ==========================================
st.markdown(
    '<div class="chat-title">🤖 FAQ Chatbot</div>',
    unsafe_allow_html=True
)

st.write("Ask any question related to the FAQ dataset.")

# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(
            f'<div class="user-message">🧑 {chat["message"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="bot-message">🤖 {chat["message"]}</div>',
            unsafe_allow_html=True
        )

# ==========================================
# CHAT INPUT
# ==========================================
user_input = st.chat_input("Type your question here...")

if user_input:

    # Store user message
    st.session_state.chat_history.append(
        {
            "role": "user",
            "message": user_input
        }
    )

    # Generate answer
    answer = get_best_answer(user_input)

    # Store bot response
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "message": answer
        }
    )

    st.rerun()

# ==========================================
# DOWNLOAD CHAT HISTORY
# ==========================================
if st.session_state.chat_history:

    chat_text = ""

    for item in st.session_state.chat_history:
        role = item["role"].upper()
        msg = item["message"]
        chat_text += f"{role}: {msg}\n\n"

    filename = (
        f"chat_history_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    st.download_button(
        label="📥 Download Chat History",
        data=chat_text,
        file_name=filename,
        mime="text/plain"
    )

# ==========================================
# FOOTER
# ==========================================
st.write("---")
st.caption(
    "Built with Python, Streamlit, TF-IDF, and Cosine Similarity"
)
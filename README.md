# 🤖 FAQ Chatbot — CodeAlpha AI Internship

A professional FAQ Chatbot built with **Python** and **Streamlit**, powered by **TF-IDF Vectorisation** and **Cosine Similarity** for intelligent question matching.

---

## ✨ Features

| Feature | Details |
|---|---|
| 💬 Chat Interface | ChatGPT-style dark-themed UI |
| 📚 FAQ Dataset | 25 curated AI / ML / Python FAQs |
| 🧠 Algorithm | TF-IDF + Cosine Similarity |
| 📊 Confidence Score | Visual confidence bar per answer |
| 🕑 Chat History | Full session history with timestamps |
| ⬇️ Download | Export chat history as CSV |
| 📋 Sidebar | Live stats and project information |
| ⚠️ Error Handling | Graceful fallback for unmatched queries |

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** — web app framework
- **Scikit-learn** — TF-IDF vectoriser & cosine similarity
- **Pandas** — data export
- **NumPy** — numerical operations

---

## ⚡ Quick Start

### 1. Clone / Download the project

```bash
git clone https://github.com/yourusername/faq-chatbot.git
cd faq-chatbot
```

### 2. Create a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**

---

## 📁 Project Structure

```
faq-chatbot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── Project_Report.md   # Detailed project report
```

---

## 🔧 How It Works

```
User Question
      │
      ▼
TF-IDF Vectorisation   ←── FAQ Questions (pre-vectorised at startup)
      │
      ▼
Cosine Similarity Computation
      │
      ▼
Best Match (score ≥ threshold) ──► Return Answer + Confidence
      │
      ▼ (score < threshold)
Fallback "No match" message
```

---

## 🧪 Sample Questions to Try

- What is artificial intelligence?
- How does TF-IDF work?
- What is cosine similarity?
- How do I run a Streamlit app?
- What is overfitting?
- What is CodeAlpha?

---

## 📜 License

This project is submitted as part of the **CodeAlpha AI Internship** program.  
Free to use for educational purposes.

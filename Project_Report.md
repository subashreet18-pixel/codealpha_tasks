# Project Report
## FAQ Chatbot — CodeAlpha AI Internship

---

## 1. Project Overview

| Item | Detail |
|---|---|
| **Project Title** | FAQ Chatbot using TF-IDF and Cosine Similarity |
| **Programme** | CodeAlpha AI Internship |
| **Technology** | Python, Streamlit, Scikit-learn |
| **Domain** | Natural Language Processing (NLP) |
| **Difficulty** | Beginner–Intermediate |

### Objective

Build a web-based FAQ chatbot that accepts natural-language questions from users and returns the most relevant answer from a predefined knowledge base using classical NLP techniques — without requiring a cloud AI API or GPU.

---

## 2. Problem Statement

Users often need quick answers to common questions. A rule-based chatbot with exact keyword matching fails when users phrase questions differently. This project solves that by computing **semantic similarity** between a user's query and all FAQ questions, returning the closest match even when wording differs.

---

## 3. Algorithm Explanation

### 3.1 TF-IDF (Term Frequency–Inverse Document Frequency)

TF-IDF converts text into numerical vectors by weighing each word's importance:

```
TF(t, d)  = (number of times term t appears in document d) /
             (total number of terms in document d)

IDF(t)    = log(total documents / documents containing term t)

TF-IDF(t, d) = TF(t, d) × IDF(t)
```

- **High TF-IDF** → word is frequent in this document but rare across all documents (distinctive).
- **Low TF-IDF** → word is common everywhere (e.g., "the", "is").

### 3.2 Cosine Similarity

Cosine similarity measures the angle θ between two TF-IDF vectors A and B:

```
cosine_similarity(A, B) = (A · B) / (‖A‖ × ‖B‖)
```

- **Result = 1.0** → identical direction (very similar text)
- **Result = 0.0** → perpendicular (no common meaningful words)

The FAQ question with the highest cosine similarity score to the user query is selected as the answer.

### 3.3 Threshold Filtering

If the best similarity score is below **0.15**, the bot returns a polite "no match" message instead of a wrong answer. This prevents false positives.

---

## 4. System Architecture

```
┌─────────────────────────────────────────────────┐
│                  Streamlit UI                   │
│   ┌─────────────┐        ┌──────────────────┐   │
│   │  Chat Panel │        │    Sidebar       │   │
│   │  (messages) │        │  (stats + info)  │   │
│   └──────┬──────┘        └──────────────────┘   │
│          │ user query                            │
└──────────┼──────────────────────────────────────┘
           │
           ▼
┌──────────────────────────┐
│   TF-IDF Vectoriser      │  ← fitted on 25 FAQ questions at startup
│   (Scikit-learn)         │    (cached with @st.cache_resource)
└──────────┬───────────────┘
           │ query vector
           ▼
┌──────────────────────────┐
│   Cosine Similarity       │  ← compares query vs all FAQ vectors
└──────────┬───────────────┘
           │ scores [0.0 – 1.0]
           ▼
┌──────────────────────────┐
│   Best Match Selector    │  ← argmax → check threshold → return answer
└──────────────────────────┘
```

---

## 5. FAQ Dataset

The chatbot includes **25 carefully curated FAQs** across five categories:

| Category | Count | Topics |
|---|---|---|
| AI & ML Fundamentals | 10 | AI, ML, DL, NLP, Neural Networks, Supervised/Unsupervised |
| Python & Streamlit | 4 | Python, Streamlit setup, running apps |
| TF-IDF & NLP | 3 | TF-IDF, Cosine Similarity, how the bot works |
| Data Science | 4 | Data Science, Overfitting, Recommendation Systems |
| Career & Internship | 4 | CodeAlpha, Skills, Chatbots, AI vs ML |

---

## 6. Key Features

### 6.1 ChatGPT-Style Interface
Custom CSS creates a dark-themed, bubble-based chat interface with avatar icons, timestamps, and a fixed input bar at the bottom.

### 6.2 Confidence Score
Each bot response shows a colour-coded confidence bar:
- 🟢 Green ≥ 50% — strong match
- 🟡 Yellow ≥ 25% — moderate match
- 🔴 Red < 25% — weak match (but above threshold)

### 6.3 Session Statistics
The sidebar tracks total queries, successful matches, and a live success-rate percentage.

### 6.4 Download Chat History
The entire conversation is exportable as a timestamped CSV file via the sidebar download button.

### 6.5 Error Handling
All TF-IDF operations are wrapped in try/except blocks. Unknown queries trigger a user-friendly fallback message rather than a crash.

---

## 7. Performance

| Metric | Value |
|---|---|
| FAQ dataset size | 25 questions |
| Vectoriser vocabulary | up to 5,000 features |
| N-gram range | Unigrams + Bigrams (1, 2) |
| Similarity threshold | 0.15 |
| Average response time | < 50 ms |
| Memory footprint | < 50 MB |

---

## 8. Installation & Execution

```bash
# Step 1 — Install dependencies
pip install -r requirements.txt

# Step 2 — Launch the app
streamlit run app.py

# App will open at http://localhost:8501
```

---

## 9. Limitations & Future Improvements

| Limitation | Future Improvement |
|---|---|
| Only matches pre-existing FAQs | Add a generative LLM backend (Claude / GPT) |
| TF-IDF ignores word order | Replace with sentence transformers (BERT) |
| No user authentication | Add login and per-user history persistence |
| Static FAQ dataset | Admin panel to add/edit FAQs dynamically |
| No voice input | Integrate Web Speech API |

---

## 10. Viva Questions & Answers

**Q1. What algorithm does this chatbot use to find the best answer?**
> It uses **TF-IDF vectorisation** to convert text into numerical vectors and **Cosine Similarity** to measure the angle between the user query vector and each FAQ vector. The FAQ with the highest similarity score is returned.

**Q2. Why is TF-IDF better than simple keyword matching?**
> Keyword matching requires exact words. TF-IDF weighs words by their importance across the entire corpus, so common words like "the" get low weights while distinctive words get high weights. This makes matching more robust to paraphrasing.

**Q3. What does a cosine similarity score of 1.0 mean?**
> It means the two vectors point in exactly the same direction — the texts are essentially identical in meaning (based on their word distributions). A score of 0 means no overlap in meaningful terms.

**Q4. Why is there a threshold of 0.15?**
> Without a threshold, the bot would always return *some* answer even for completely unrelated questions. The 0.15 threshold means: "if the best match score is below 15%, the query is too different from all FAQs — return a fallback message."

**Q5. What is `@st.cache_resource` used for?**
> It caches the TF-IDF vectoriser and the pre-computed FAQ matrix so they are only built once when the app starts, not on every user interaction. This dramatically improves performance.

**Q6. What is the difference between TF and IDF?**
> **TF (Term Frequency)** measures how often a word appears in one document. **IDF (Inverse Document Frequency)** measures how rare that word is across all documents. Multiplying them gives a score that rewards distinctive, informative words.

**Q7. Why did you use bigrams (ngram_range=(1,2)) in the TF-IDF vectoriser?**
> Bigrams capture two-word phrases like "machine learning" or "cosine similarity" as single features, preserving meaning that would be lost if each word were treated independently.

**Q8. How does the confidence bar colour change?**
> The colour is computed from the cosine similarity score: green for ≥ 50% (strong match), yellow for ≥ 25% (moderate), and red for below 25% (weak but above threshold).

**Q9. What Python libraries are used and why?**
> - **Streamlit** — builds the web UI with pure Python.  
> - **Scikit-learn** — provides `TfidfVectorizer` and `cosine_similarity`.  
> - **Pandas** — converts chat history to a DataFrame for CSV export.  
> - **NumPy** — `argmax` finds the index of the highest similarity score.

**Q10. How would you scale this chatbot to handle 10,000 FAQs?**
> For large datasets, computing cosine similarity against every vector sequentially becomes slow. Solutions include: (1) approximate nearest-neighbour search (FAISS, Annoy), (2) replacing TF-IDF with dense embeddings (sentence-transformers) and vector databases (Pinecone, Weaviate), or (3) indexing with BM25 (rank_bm25 library).

---

## 11. Conclusion

This project demonstrates a complete end-to-end NLP pipeline — from raw text to an interactive web application — using only lightweight, beginner-accessible libraries. TF-IDF and Cosine Similarity are foundational techniques that underpin modern search engines and recommendation systems, making this an excellent learning project for AI internship candidates.

---

*Submitted for CodeAlpha AI Internship | Built with Python, Streamlit & Scikit-learn*

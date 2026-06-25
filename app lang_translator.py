# ============================================================
# Language Translation Tool
# Author: CodeAlpha AI Internship Project
# Description: A professional language translation tool built
#              with Streamlit featuring auto-detection, TTS,
#              history tracking, and modern UI.
# ============================================================

import streamlit as st
import json
import datetime
import base64
from pathlib import Path
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
from gtts import gTTS
import io
import tempfile

# ── Reproducibility for language detection ──────────────────
DetectorFactory.seed = 42

# ── Page configuration ──────────────────────────────────────
st.set_page_config(
    page_title="SmartTranslate AI – Language Translation Tool",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Language data ────────────────────────────────────────────
# Mapping of display names → deep-translator language codes
LANGUAGES = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am",
    "Arabic": "ar", "Armenian": "hy", "Azerbaijani": "az",
    "Basque": "eu", "Belarusian": "be", "Bengali": "bn",
    "Bosnian": "bs", "Bulgarian": "bg", "Catalan": "ca",
    "Cebuano": "ceb", "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW", "Croatian": "hr",
    "Czech": "cs", "Danish": "da", "Dutch": "nl",
    "English": "en", "Esperanto": "eo", "Estonian": "et",
    "Finnish": "fi", "French": "fr", "Galician": "gl",
    "Georgian": "ka", "German": "de", "Greek": "el",
    "Gujarati": "gu", "Haitian Creole": "ht", "Hausa": "ha",
    "Hebrew": "iw", "Hindi": "hi", "Hmong": "hmn",
    "Hungarian": "hu", "Icelandic": "is", "Igbo": "ig",
    "Indonesian": "id", "Irish": "ga", "Italian": "it",
    "Japanese": "ja", "Javanese": "jw", "Kannada": "kn",
    "Kazakh": "kk", "Khmer": "km", "Korean": "ko",
    "Kurdish": "ku", "Kyrgyz": "ky", "Lao": "lo",
    "Latin": "la", "Latvian": "lv", "Lithuanian": "lt",
    "Luxembourgish": "lb", "Macedonian": "mk", "Malagasy": "mg",
    "Malay": "ms", "Malayalam": "ml", "Maltese": "mt",
    "Maori": "mi", "Marathi": "mr", "Mongolian": "mn",
    "Myanmar (Burmese)": "my", "Nepali": "ne", "Norwegian": "no",
    "Nyanja (Chichewa)": "ny", "Pashto": "ps", "Persian": "fa",
    "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa",
    "Romanian": "ro", "Russian": "ru", "Samoan": "sm",
    "Scots Gaelic": "gd", "Serbian": "sr", "Sesotho": "st",
    "Shona": "sn", "Sindhi": "sd", "Sinhala": "si",
    "Slovak": "sk", "Slovenian": "sl", "Somali": "so",
    "Spanish": "es", "Sundanese": "su", "Swahili": "sw",
    "Swedish": "sv", "Tajik": "tg", "Tamil": "ta",
    "Telugu": "te", "Thai": "th", "Turkish": "tr",
    "Ukrainian": "uk", "Urdu": "ur", "Uzbek": "uz",
    "Vietnamese": "vi", "Welsh": "cy", "Xhosa": "xh",
    "Yiddish": "yi", "Yoruba": "yo", "Zulu": "zu",
}

# Reverse mapping: code → display name
CODE_TO_NAME = {v: k for k, v in LANGUAGES.items()}

# ── Custom CSS ───────────────────────────────────────────────
def inject_css():
    """Inject custom CSS for a modern, polished UI."""
    st.markdown("""
    <style>
    /* ── Global ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Background ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* ── Hero header ── */
    .hero-header {
        text-align: center;
        padding: 2.5rem 1rem 1rem;
        animation: fadeInDown 0.8s ease;
    }
    .hero-header h1 {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .hero-header p {
        color: #94a3b8;
        font-size: 1.1rem;
        margin: 0;
    }

    /* ── Cards ── */
    .card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
    }

    /* ── Detected badge ── */
    .detected-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: linear-gradient(135deg, #7c3aed, #2563eb);
        color: white;
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.75rem;
    }

    /* ── Translation output box ── */
    .translation-box {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 1.25rem;
        min-height: 120px;
        color: #e2e8f0;
        font-size: 1.05rem;
        line-height: 1.7;
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    /* ── Stat chips ── */
    .stat-chip {
        display: inline-block;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 8px;
        padding: 0.3rem 0.8rem;
        font-size: 0.78rem;
        color: #94a3b8;
        margin: 0.2rem;
    }

    /* ── History item ── */
    .history-item {
        background: rgba(255,255,255,0.04);
        border-left: 3px solid #7c3aed;
        border-radius: 0 10px 10px 0;
        padding: 0.9rem 1rem;
        margin-bottom: 0.6rem;
        transition: background 0.2s;
    }
    .history-item:hover { background: rgba(255,255,255,0.07); }
    .history-meta {
        color: #64748b;
        font-size: 0.75rem;
        margin-bottom: 0.3rem;
    }
    .history-src { color: #94a3b8; font-size: 0.9rem; }
    .history-tgt { color: #a78bfa; font-size: 0.9rem; font-weight: 500; }

    /* ── Section labels ── */
    .section-label {
        color: #7c3aed;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.4rem;
    }

    /* ── Streamlit overrides ── */
    .stTextArea textarea {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: black !important;
        font-size: 1rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124,58,237,0.25) !important;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        border: none !important;
    }
    .stButton > button:hover { transform: translateY(-1px) !important; }

    /* Primary translate button */
    div[data-testid="stHorizontalBlock"] .stButton:first-child > button {
        background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
        color: white !important;
        padding: 0.6rem 2rem !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15,12,41,0.9) !important;
        border-right: 1px solid rgba(255,255,255,0.08) !important;
    }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }

    /* Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; } to { opacity: 1; }
    }
    .fade-in { animation: fadeIn 0.5s ease; }

    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


# ── Session state initialiser ─────────────────────────────────
def init_session_state():
    """Initialise all required session-state keys once."""
    defaults = {
        "history": [],          # list of translation records
        "translated_text": "",  # latest translation output
        "detected_lang": None,  # ISO code of detected language
        "char_count": 0,        # source character count
        "word_count": 0,        # source word count
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ── Language detection ────────────────────────────────────────
def detect_language(text: str) -> str | None:
    """
    Detect the language of *text* using langdetect.
    Returns an ISO 639-1 code or None on failure.
    """
    try:
        if text.strip():
            return detect(text)
    except Exception:
        pass
    return None


# ── Translation ───────────────────────────────────────────────
def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate *text* from source_lang → target_lang via Google Translate.
    Returns the translated string or raises an exception with a user-
    friendly message.
    """
    if not text.strip():
        raise ValueError("Please enter some text to translate.")
    if source_lang == target_lang:
        raise ValueError("Source and target languages must be different.")

    translator = GoogleTranslator(source=source_lang, target=target_lang)
    result = translator.translate(text)
    if not result:
        raise ValueError("Translation returned empty. Please try again.")
    return result


# ── Text-to-Speech ────────────────────────────────────────────
def text_to_speech(text: str, lang_code: str) -> bytes:
    """
    Convert *text* to MP3 audio bytes using gTTS.
    Some language codes used by Google Translate differ from gTTS codes;
    we handle the common mismatches here.
    """
    # gTTS uses slightly different codes for a few languages
    tts_code_map = {
        "zh-CN": "zh",
        "zh-TW": "zh-TW",
        "iw": "iw",      # Hebrew
        "jw": "jw",      # Javanese
    }
    tts_lang = tts_code_map.get(lang_code, lang_code)

    tts = gTTS(text=text, lang=tts_lang, slow=False)
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer.read()


# ── Download helper ───────────────────────────────────────────
def get_text_download_link(text: str, filename: str = "translation.txt") -> str:
    """Return an HTML <a> tag that triggers a .txt file download."""
    b64 = base64.b64encode(text.encode()).decode()
    return (
        f'<a href="data:text/plain;base64,{b64}" '
        f'download="{filename}" '
        f'style="text-decoration:none;">'
        f'<button style="background:linear-gradient(135deg,#7c3aed,#2563eb);'
        f'color:white;border:none;padding:0.45rem 1.2rem;border-radius:8px;'
        f'font-weight:600;cursor:pointer;font-size:0.9rem;">⬇ Download</button>'
        f'</a>'
    )


# ── Sidebar ───────────────────────────────────────────────────
def render_sidebar():
    """Render the sidebar with stats and settings."""
    with st.sidebar:
        st.markdown("## 🌐 SmartTranslate AI")
        st.markdown("*Professional Translation Tool*")
        st.divider()

        # Session statistics
        st.markdown("### 📊 Session Stats")
        total = len(st.session_state.history)
        langs_used = set()
        for h in st.session_state.history:
            langs_used.add(h.get("target"))
        st.metric("Total Translations", total)
        st.metric("Languages Used", len(langs_used))

        st.divider()
        st.markdown("### ℹ️ About")
        st.markdown(
            "SmartTranslate AI supports **108 languages** powered by Google Translate. "
            "Text-to-speech is available for most major languages."
        )
        st.divider()

        # Clear history button
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.success("History cleared!")


# ── Main UI ───────────────────────────────────────────────────
def render_main():
    """Render the primary translation interface."""

    # Hero header
    st.markdown("""
    <div class="hero-header">
        <h1>🌐 SmartTranslate AI</h1>
        <p>Instant, intelligent language translation powered by AI</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Input card ──────────────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">📝 Source Text</p>', unsafe_allow_html=True)

    source_text = st.text_area(
        label="Source Text",
        placeholder="Type or paste text here…",
        height=160,
        label_visibility="collapsed",
        key="source_input",
    )

    # Live character / word count
    if source_text:
        char_count = len(source_text)
        word_count = len(source_text.split())
        st.markdown(
            f'<span class="stat-chip">✏️ {char_count} characters</span>'
            f'<span class="stat-chip">📖 {word_count} words</span>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Language selectors ──────────────────────────────────
    lang_names = list(LANGUAGES.keys())

    col1, col_arrow, col2 = st.columns([5, 1, 5])

    with col1:
        st.markdown('<p class="section-label">🔍 Source Language</p>', unsafe_allow_html=True)
        use_auto = st.checkbox("Auto-detect", value=True, key="auto_detect")
        if use_auto:
            source_lang_name = None   # will detect at runtime
        else:
            source_lang_name = st.selectbox(
                "Source language",
                lang_names,
                index=lang_names.index("English"),
                label_visibility="collapsed",
            )

    with col_arrow:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center;font-size:1.8rem;color:#7c3aed;padding-top:0.5rem;">⇄</div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown('<p class="section-label">🎯 Target Language</p>', unsafe_allow_html=True)
        default_target = lang_names.index("Spanish")
        target_lang_name = st.selectbox(
            "Target language",
            lang_names,
            index=default_target,
            label_visibility="collapsed",
            key="target_lang",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Action buttons ──────────────────────────────────────
    btn_col1, btn_col2, btn_col3 = st.columns([3, 1, 1])

    with btn_col1:
        translate_clicked = st.button(
            "🚀 Translate",
            use_container_width=True,
            type="primary",
        )

    with btn_col2:
        clear_clicked = st.button("🔄 Clear", use_container_width=True)

    with btn_col3:
        swap_clicked = st.button("⇄ Swap", use_container_width=True)

    # Handle swap (swap target to source, clear output)
    if swap_clicked and st.session_state.translated_text:
        # We can't programmatically set the text_area value easily,
        # so we store the swap request and show a message.
        st.info(
            f"💡 Copy the translation below and paste it as your source text, "
            f"then set source → **{target_lang_name}**."
        )

    # Handle clear
    if clear_clicked:
        st.session_state.translated_text = ""
        st.session_state.detected_lang = None
        st.rerun()

    # ── Translation logic ───────────────────────────────────
    if translate_clicked:
        if not source_text.strip():
            st.warning("⚠️ Please enter some text before translating.")
        else:
            with st.spinner("Translating…"):
                try:
                    # Determine source language code
                    if use_auto:
                        detected_code = detect_language(source_text)
                        if detected_code:
                            st.session_state.detected_lang = detected_code
                            src_code = detected_code
                        else:
                            st.warning("Could not detect language; defaulting to English.")
                            src_code = "en"
                            st.session_state.detected_lang = "en"
                    else:
                        src_code = LANGUAGES[source_lang_name]
                        st.session_state.detected_lang = src_code

                    tgt_code = LANGUAGES[target_lang_name]

                    # Perform translation
                    result = translate_text(source_text, src_code, tgt_code)
                    st.session_state.translated_text = result

                    # Save to history (newest first)
                    st.session_state.history.insert(0, {
                        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                        "source_text": source_text[:120] + ("…" if len(source_text) > 120 else ""),
                        "translated_text": result[:120] + ("…" if len(result) > 120 else ""),
                        "source": CODE_TO_NAME.get(src_code, src_code),
                        "target": target_lang_name,
                    })

                    # Keep only the last 20 entries
                    st.session_state.history = st.session_state.history[:20]

                except ValueError as e:
                    st.error(f"❌ {e}")
                except Exception as e:
                    st.error(f"❌ Translation failed: {e}")

    # ── Output card ─────────────────────────────────────────
    if st.session_state.translated_text:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">✨ Translation</p>', unsafe_allow_html=True)

        # Show detected language badge
        if st.session_state.detected_lang and use_auto:
            detected_name = CODE_TO_NAME.get(
                st.session_state.detected_lang, st.session_state.detected_lang
            )
            st.markdown(
                f'<span class="detected-badge">🔍 Detected: {detected_name}</span>',
                unsafe_allow_html=True,
            )

        # Render translated text
        st.markdown(
            f'<div class="translation-box">{st.session_state.translated_text}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Action row: TTS | Download
        act_col1, act_col2, act_col3 = st.columns([2, 2, 4])

        with act_col1:
            if st.button("🔊 Listen", use_container_width=True):
                with st.spinner("Generating audio…"):
                    try:
                        tgt_code = LANGUAGES[target_lang_name]
                        audio_bytes = text_to_speech(
                            st.session_state.translated_text, tgt_code
                        )
                        st.audio(audio_bytes, format="audio/mp3")
                    except Exception as e:
                        st.error(f"TTS not available for this language: {e}")

        with act_col2:
            # Build download link
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"translation_{timestamp}.txt"
            download_content = (
                f"Source Text:\n{source_text}\n\n"
                f"Translated Text ({target_lang_name}):\n"
                f"{st.session_state.translated_text}\n\n"
                f"Translated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            st.markdown(
                get_text_download_link(download_content, filename),
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)


# ── History panel ─────────────────────────────────────────────
def render_history():
    """Render the translation history section."""
    if not st.session_state.history:
        return

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🕑 Translation History")
    st.markdown(f"*Showing last {len(st.session_state.history)} translations*")

    for item in st.session_state.history:
        st.markdown(f"""
        <div class="history-item">
            <div class="history-meta">
                🕐 {item['timestamp']} &nbsp;|&nbsp;
                {item['source']} → {item['target']}
            </div>
            <div class="history-src">📄 {item['source_text']}</div>
            <div class="history-tgt">✨ {item['translated_text']}</div>
        </div>
        """, unsafe_allow_html=True)


# ── Entry point ───────────────────────────────────────────────
def main():
    inject_css()
    init_session_state()
    render_sidebar()
    render_main()
    render_history()


if __name__ == "__main__":
    main()

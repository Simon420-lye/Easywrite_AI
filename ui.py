import streamlit as st
import requests

BACKEND = "https://easywrite-ai.onrender.com"

# ---------------------- BRANDING + PAGE CONFIG ----------------------
st.set_page_config(
    page_title="RoRoWrites HumanAizer",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------- CUSTOM CSS (WHITE THEME + BLACK TEXT) ----------------------
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }
    *, div, p, span, label {
        color: #000000 !important;
    }
    textarea, input, select {
        background-color: #f5f5f5 !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #f5f5f5 !important;
        border: 1px solid #cccccc !important;
        color: #000000 !important;
    }
    .title-banner {
        padding: 20px;
        border-radius: 12px;
        background: linear-gradient(90deg, #ffffff, #f8f8f8);
        text-align: center;
        color: #000000;
        font-size: 38px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 20px;
        border: 1px solid #ddd;
    }
    button[kind="primary"] {
        background-color: #000000 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
    }
    button[kind="primary"]:hover {
        background-color: #333333 !important;
    }
    .footer {
        margin-top: 60px;
        text-align: center;
        padding: 12px;
        color: #666;
        font-size: 14px;
        border-top: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- HEADER ----------------------
st.markdown(
    '<div class="title-banner"> RoRoWrites HumanAizer</div>',
    unsafe_allow_html=True
)

# ---------------------- SIDEBAR ----------------------
st.sidebar.title("⚡ RoRoWrites")
option = st.sidebar.selectbox(
    "Choose Function:",
    ["Rewrite", "Plagiarism Check", "AI Detection", "Generate Unique Content"]
)

st.sidebar.write("---")
st.sidebar.write("🔥 Designed for Lazy Students")
st.sidebar.write("🎓 100% Humanized Assignments")
st.sidebar.write("🛡️ Zero AI Detection • Zero Plagiarism")
st.sidebar.write("📝 No word limits, go beyond")

# ---------------------- MAIN INPUT ----------------------
text = st.text_area("✍️ Enter your text here:", height=200)

if st.button("Process 🚀"):

    # --------------------------------------------------------
    #  REWRITE SECTION (SIDE-BY-SIDE COMPARISON)
    # --------------------------------------------------------
    if option == "Rewrite":
        res = requests.post(f"{BACKEND}/rewrite", json={"text": text}).json()
        rewritten = res.get("rewritten_text", "")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔵 Original Text")
            st.write(text)

        with col2:
            st.subheader("🟢 Humanized Rewrite (AI-Free)")
            st.write(rewritten)
             
             # copy to Clipboard
            if st.button("copy to clipboard"):
                st.clipboard_set(rewritten)
                st.success("✓ Text copied to clipboard")

    # --------------------------------------------------------
    #  PLAGIARISM CHECK (HUMAN-FRIENDLY RESULT)
    # --------------------------------------------------------
    elif option == "Plagiarism Check":
        res = requests.post(f"{BACKEND}/plagiarism", json={"text": text}).json()
        result = res.get("plagiarism_result", {"similarity_score": 0, "explanation": "No data"})

        score = result.get("similarity_score", 0)
        explanation = result.get("explanation", "No explanation available.")

        st.subheader("📚 Plagiarism Report")

        if score < 10:
            st.success("🟢 Fully Original — 0–10% similarity")
        elif score < 30:
            st.warning("🟡 Mild Overlap — 10–30% similarity")
        else:
            st.error("🔴 High Similarity — Rewrite Required")

        st.write(f"### 🔍 Similarity Score: **{score}%**")
        st.write(f"### 📝 Explanation:\n{explanation}")

    # --------------------------------------------------------
    #  AI DETECTION (ROBUST + HUMAN-FRIENDLY)
    # --------------------------------------------------------
    elif option == "AI Detection":
        res = requests.post(f"{BACKEND}/ai_detect", json={"text": text}).json()

        ai_data = res.get("ai_detection", {})
        if "error" in ai_data:
            st.error(f"Error: {ai_data['error']}")
        else:
            ai_scores = ai_data.get("scores", {"ai_score": 0, "human_score": 100})
            readable_summary = ai_data.get("readable", "No summary available.")

            ai_score = ai_scores.get("ai_score", 0)
            human_score = ai_scores.get("human_score", 100)

            st.subheader("🤖 AI Detection Report")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("AI Written Content", f"{ai_score}%")
                st.metric("Human Written Content", f"{human_score}%")
            with col2:
                st.progress(human_score / 100)

            st.markdown(readable_summary)

            if ai_score < 20:
                st.success("🟢 100% Human — Natural writing detected.")
            elif ai_score < 60:
                st.warning("🟡 Mixed — Some AI patterns detected.")
            else:
                st.error("🔴 Likely AI — Rewrite with RoRoWrites.")

    # --------------------------------------------------------
    #  GENERATE UNIQUE CONTENT
    # --------------------------------------------------------
    else:
        res = requests.post(f"{BACKEND}/generate", json={"text": text}).json()
        st.subheader("✨ Generated Unique Text")
        st.write(res.get("generated_unique_text", ""))

# ---------------------- FOOTER ----------------------
st.markdown("""
<div class="footer">
    © 2025 RoRoWrites HumanAizer • Zero-AI, Zero-Plagiarism Writing Engine
</div>
""", unsafe_allow_html=True)

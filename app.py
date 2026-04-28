import streamlit as st
from model import calculate_similarity, get_missing_skills
from utils import extract_text_from_pdf

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# 🎨 Dynamic CSS
st.markdown("""
<style>

/* Background */
.main {
    background: linear-gradient(120deg, #0f172a, #020617);
}

/* Hero section */
.hero {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
}

/* Big score */
.score {
    font-size: 60px;
    font-weight: bold;
    text-align: center;
    color: #38bdf8;
}

/* Tag style */
.tag {
    display: inline-block;
    background: #1e293b;
    color: #38bdf8;
    padding: 6px 12px;
    margin: 5px;
    border-radius: 20px;
    font-size: 14px;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-weight: bold;
    border: none;
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
}

</style>
""", unsafe_allow_html=True)

# 🚀 HERO HEADER
st.markdown("""
<div class="hero">
    <h1>🚀 AI Resume Analyzer</h1>
    <p>Match your resume with job roles using AI</p>
</div>
""", unsafe_allow_html=True)

# 📥 INPUT SECTION
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf"])

with col2:
    jd_text = st.text_area("🧾 Paste Job Description")

st.write("")

# 🔍 BUTTON
if st.button("🔍 Analyze Resume"):

    if uploaded_file and jd_text:

        resume_text = extract_text_from_pdf(uploaded_file)

        score = calculate_similarity(resume_text, jd_text)
        missing_skills = get_missing_skills(resume_text, jd_text)

        st.markdown("---")

        # 🎯 BIG SCORE DISPLAY
        st.markdown(f'<div class="score">{score}%</div>', unsafe_allow_html=True)
        st.progress(int(score))

        # Feedback
        if score > 75:
            st.success("Excellent match 🚀")
        elif score > 50:
            st.warning("Decent match, can improve ⚡")
        else:
            st.error("Low match, needs work ❌")

        st.markdown("---")

        # 📊 TWO COLUMN SECTION
        col3, col4 = st.columns(2)

        # 🧠 Missing Skills (TAGS UI)
        with col3:
            st.subheader("🧠 Missing Skills")

            if missing_skills:
                tags_html = "".join([f'<span class="tag">{skill}</span>' for skill in missing_skills])
                st.markdown(tags_html, unsafe_allow_html=True)
            else:
                st.success("No major gaps 🎯")

        # 🔑 Keywords (TAGS UI)
        with col4:
            st.subheader("🔑 Resume Keywords")

            resume_words = list(set(resume_text.lower().split()))[:20]
            tags_html = "".join([f'<span class="tag">{word}</span>' for word in resume_words])
            st.markdown(tags_html, unsafe_allow_html=True)

    else:
        st.warning("Upload resume and paste job description ⚠️")
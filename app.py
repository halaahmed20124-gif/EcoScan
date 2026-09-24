import os
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
from PIL import Image

from waste_knowledge import get_waste_info, get_biotech_info, calculate_eco_points
from ai_assistant import assistant_response
from history_manager import (
    init_database,
    save_analysis,
    get_history,
    delete_analysis,
    clear_history,
)

# ============================================================
# EcoScan — AI-Powered Waste Management Assistant
# UI/UX redesign only: core project logic preserved
# ============================================================

st.set_page_config(
    page_title="EcoScan",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# ECO-TECH STYLE
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --eco-green: #1f8f5f;
    --eco-dark: #123b2a;
    --eco-light: #eaf8f0;
    --eco-mint: #dff5e8;
    --eco-blue: #5b7cfa;
    --eco-text: #17352a;
    --eco-muted: #6d7f76;
    --eco-border: #dcebe2;
    --eco-white: #ffffff;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #f7fcf9 0%, #ffffff 55%, #f6fbf8 100%);
    color: var(--eco-text);
}

.block-container {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f1faf5 100%);
    border-right: 1px solid var(--eco-border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem;
}

.eco-brand {
    padding: 14px 12px 20px 12px;
    text-align: center;
}

.eco-logo {
    width: 58px;
    height: 58px;
    margin: auto;
    border-radius: 18px;
    background: linear-gradient(135deg, #1f8f5f, #5fbd83);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    box-shadow: 0 10px 25px rgba(31,143,95,.18);
}

.eco-brand-title {
    font-size: 25px;
    font-weight: 800;
    color: var(--eco-dark);
    margin-top: 10px;
}

.eco-brand-subtitle {
    color: var(--eco-muted);
    font-size: 12px;
    margin-top: 3px;
}

.eco-hero {
    border-radius: 28px;
    padding: 34px;
    background: linear-gradient(135deg, #e9f8ef 0%, #f8fffb 55%, #eef7ff 100%);
    border: 1px solid var(--eco-border);
    box-shadow: 0 15px 40px rgba(24,75,51,.07);
    margin-bottom: 24px;
}

.eco-kicker {
    color: var(--eco-green);
    font-weight: 700;
    font-size: 14px;
    letter-spacing: .4px;
    text-transform: uppercase;
}

.eco-hero h1 {
    font-size: clamp(32px, 5vw, 58px);
    line-height: 1.05;
    color: var(--eco-dark);
    margin: 8px 0 12px;
    font-weight: 800;
}

.eco-hero p {
    color: var(--eco-muted);
    font-size: 16px;
    line-height: 1.7;
    max-width: 780px;
}

.eco-title {
    font-size: 32px;
    font-weight: 800;
    color: var(--eco-dark);
    margin: 5px 0 8px;
}

.eco-subtitle {
    color: var(--eco-muted);
    margin-bottom: 22px;
}

.eco-card {
    background: rgba(255,255,255,.95);
    border: 1px solid var(--eco-border);
    border-radius: 20px;
    padding: 20px;
    margin: 8px 0;
    box-shadow: 0 8px 25px rgba(18,59,42,.055);
}

.eco-card h3 {
    color: var(--eco-dark);
    margin-top: 0;
}

.eco-stat {
    background: #ffffff;
    border: 1px solid var(--eco-border);
    border-radius: 18px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 8px 25px rgba(18,59,42,.05);
}

.eco-stat-value {
    font-size: 30px;
    font-weight: 800;
    color: var(--eco-green);
}

.eco-stat-label {
    color: var(--eco-muted);
    font-size: 13px;
    margin-top: 4px;
}

.eco-feature {
    background: #ffffff;
    border: 1px solid var(--eco-border);
    border-radius: 18px;
    padding: 20px;
    min-height: 155px;
    box-shadow: 0 8px 25px rgba(18,59,42,.04);
}

.eco-feature-icon {
    font-size: 27px;
    margin-bottom: 10px;
}

.eco-feature-title {
    color: var(--eco-dark);
    font-weight: 750;
    font-size: 17px;
}

.eco-feature-text {
    color: var(--eco-muted);
    font-size: 13px;
    line-height: 1.6;
    margin-top: 7px;
}

.eco-result {
    background: linear-gradient(135deg, #e9f8ef, #ffffff);
    border: 1px solid #cfe9da;
    border-radius: 24px;
    padding: 25px;
    box-shadow: 0 12px 30px rgba(31,143,95,.08);
}

.eco-result-type {
    color: var(--eco-dark);
    font-size: 30px;
    font-weight: 800;
}

.eco-pill {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 999px;
    background: var(--eco-light);
    color: var(--eco-green);
    font-size: 12px;
    font-weight: 700;
    margin: 4px 4px 4px 0;
}

.eco-score {
    border-radius: 18px;
    padding: 18px;
    background: #fff;
    border: 1px solid var(--eco-border);
    text-align: center;
}

.eco-score-number {
    font-size: 42px;
    font-weight: 800;
    color: var(--eco-green);
}

.eco-chat {
    background: linear-gradient(135deg, #effaf4, #ffffff);
    border: 1px solid var(--eco-border);
    border-radius: 22px;
    padding: 22px;
    margin-top: 14px;
}

.eco-footer {
    text-align: center;
    color: #71827a;
    font-size: 13px;
    padding: 28px 10px 8px;
    margin-top: 35px;
    border-top: 1px solid var(--eco-border);
}

div.stButton > button {
    border-radius: 12px;
    border: 1px solid var(--eco-border);
    font-weight: 650;
    min-height: 44px;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1f8f5f, #36a96f);
    color: white;
    border: none;
}

.stDownloadButton > button {
    border-radius: 12px !important;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid var(--eco-border);
    padding: 15px;
    border-radius: 16px;
}

[data-testid="stFileUploader"] {
    background: #fbfefc;
    border-radius: 16px;
}

hr {
    border-color: var(--eco-border);
}

.small-muted {
    color: var(--eco-muted);
    font-size: 13px;
}

.success-box {
    padding: 13px 16px;
    border-radius: 13px;
    background: #eaf8f0;
    border: 1px solid #cbe8d7;
    color: #17623f;
    margin: 10px 0;
}

.warning-box {
    padding: 13px 16px;
    border-radius: 13px;
    background: #fff8e7;
    border: 1px solid #f0dfad;
    color: #7b5b0b;
    margin: 10px 0;
}

@media (max-width: 800px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .eco-hero {
        padding: 24px;
        border-radius: 22px;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# TEXT
# ============================================================

TEXT = {
    "en": {
        "home": "🏠 Home",
        "scan": "📸 Scan",
        "assistant": "🤖 AI Assistant",
        "history": "📋 History",
        "dashboard": "📊 Dashboard",
        "campus": "🏫 Campus Mode",
        "about": "ℹ️ About",
        "language": "Language",
    },
    "ar": {
        "home": "🏠 الرئيسية",
        "scan": "📸 فحص",
        "assistant": "🤖 المساعد الذكي",
        "history": "📋 السجل",
        "dashboard": "📊 لوحة البيانات",
        "campus": "🏫 وضع الجامعة",
        "about": "ℹ️ عن EcoScan",
        "language": "اللغة",
    },
}

# ============================================================
# DATABASE / MODEL
# ============================================================

init_database()

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("ecoscan_improved.keras")

try:
    model = load_model()
    model_error = None
except Exception as e:
    model = None
    model_error = str(e)

def load_class_names():
    if os.path.exists("class_names.txt"):
        with open("class_names.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return [
        "Cardboard", "Food Organics", "Glass", "Metal",
        "Miscellaneous Trash", "Paper", "Plastic",
        "Textile Trash", "Vegetation"
    ]

class_names = load_class_names()

def predict_waste(input_image):
    if model is None:
        return []
    image = input_image.convert("RGB").resize((224, 224))
    arr = np.array(image, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)
    prediction = model.predict(arr, verbose=0)[0]
    top_indices = np.argsort(prediction)[::-1][:3]
    return [
        (class_names[i], float(prediction[i] * 100))
        for i in top_indices
    ]

def confidence_info(confidence):
    if confidence >= 80:
        return "High", "🟢"
    if confidence >= 60:
        return "Medium", "🟡"
    return "Low", "🔴"

def save_scan_image(image):
    os.makedirs("scan_images", exist_ok=True)
    filename = datetime.now().strftime("scan_%Y%m%d_%H%M%S_%f.jpg")
    path = os.path.join("scan_images", filename)
    image.convert("RGB").save(path, "JPEG", quality=90)
    return path

def safe_percent(value, total):
    return round((value / total) * 100, 1) if total else 0

# ============================================================
# ECOSCAN NAVIGATION
# Same pages/functions — presentation only
# ============================================================

# Hide Streamlit's default sidebar so the interface stays closer
# to the agreed EcoScan mobile-style reference.
st.markdown("""
<style>
section[data-testid="stSidebar"] {display: none !important;}
button[kind="header"] {display: none !important;}

.eco-topbar {
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:10px 4px 18px;
}
.eco-top-brand {
    display:flex;
    align-items:center;
    gap:10px;
}
.eco-mini-logo {
    width:42px;height:42px;border-radius:13px;
    background:linear-gradient(135deg,#1f8f5f,#58bd7f);
    display:flex;align-items:center;justify-content:center;
    font-size:23px;
}
.eco-mini-name {
    font-size:22px;font-weight:800;color:#123b2a;
}
.eco-mini-sub {
    font-size:10px;color:#6d7f76;margin-top:-2px;
}
.eco-nav {
    background:rgba(255,255,255,.96);
    border:1px solid #dcebe2;
    border-radius:18px;
    padding:8px;
    box-shadow:0 8px 25px rgba(18,59,42,.06);
    margin-bottom:22px;
}
.eco-nav-label {
    color:#6d7f76;font-size:11px;margin:0 0 6px 4px;
}
@media (max-width: 700px) {
    .eco-mini-name {font-size:19px;}
    .eco-mini-sub {display:none;}
    .block-container {padding-top:.55rem !important;}
}
</style>
""", unsafe_allow_html=True)

# Keep the exact same seven destinations.
nav_items = [
    ("🏠", "Home"),
    ("📸", "Scan"),
    ("🤖", "AI Assistant"),
    ("📋", "History"),
    ("📊", "Dashboard"),
    ("🏫", "Campus Mode"),
    ("ℹ️", "About"),
]

if "eco_page" not in st.session_state:
    st.session_state["eco_page"] = "Home"

# Preserve language choice while moving it out of the sidebar.
if "eco_language" not in st.session_state:
    st.session_state["eco_language"] = "English"

st.markdown("""
<div class="eco-topbar">
    <div class="eco-top-brand">
        <div class="eco-mini-logo">♻️</div>
        <div>
            <div class="eco-mini-name">EcoScan</div>
            <div class="eco-mini-sub">AI-Powered Waste Management Assistant</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

lang_col, nav_col = st.columns([1, 5])

with lang_col:
    language = st.radio(
        "Language / اللغة",
        ["English", "العربية"],
        index=0 if st.session_state["eco_language"] == "English" else 1,
        horizontal=True,
        label_visibility="collapsed",
        key="eco_language_radio",
    )
    st.session_state["eco_language"] = language
    lang = "ar" if language == "العربية" else "en"

with nav_col:
    labels = [f"{icon} {name}" for icon, name in nav_items]
    current_label = next(
        f"{icon} {name}" for icon, name in nav_items
        if name == st.session_state["eco_page"]
    )
    selected = st.radio(
        "Navigation",
        labels,
        index=labels.index(current_label),
        horizontal=True,
        label_visibility="collapsed",
        key="eco_navigation",
    )
    selected_name = selected.split(" ", 1)[1]
    st.session_state["eco_page"] = selected_name

page = st.session_state["eco_page"]

# ============================================================
# HOME
# ============================================================

if page == TEXT[lang]["home"]:

    st.markdown("""
    <div class="eco-hero">
        <div class="eco-kicker">AI • Sustainability • Smart Campus</div>
        <h1>EcoScan</h1>
        <p>
            AI-Powered Waste Management Assistant designed to help identify
            waste, understand its environmental impact, choose a suitable
            action, and build useful campus waste insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 1])

    with c1:
        st.markdown("""
        <div class="eco-card">
            <h3>🌱 From image to action</h3>
            <p class="small-muted">
                Upload a waste image, let the trained model classify it,
                then use EcoScan's knowledge base for recommendations,
                EcoScore, environmental information and biotechnology pathways.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📸 Start Scanning", type="primary", use_container_width=True):
            st.session_state["eco_page"] = "Scan"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="eco-card">
            <h3>🧠 What makes EcoScan specialized?</h3>
            <p class="small-muted">
                EcoScan combines AI classification with a waste knowledge base,
                recommendations, history, campus analytics and an educational
                assistant rather than acting as a general image chatbot.
            </p>
        </div>
        """, unsafe_allow_html=True)

    history = get_history()
    total = len(history)
    recyclable = sum(
        bool(get_waste_info(r[2]).get("recyclable", False)) for r in history
    )

    st.markdown("### 📊 EcoScan at a glance")
    a, b, c, d = st.columns(4)

    stats = [
        ("🧠", "AI Accuracy", "80.62%"),
        ("🗂️", "Waste Categories", "9"),
        ("📸", "Total Scans", str(total)),
        ("♻️", "Recyclable Scans", str(recyclable)),
    ]

    for col, (icon, label, value) in zip([a,b,c,d], stats):
        with col:
            st.markdown(
                f'<div class="eco-stat"><div>{icon}</div>'
                f'<div class="eco-stat-value">{value}</div>'
                f'<div class="eco-stat-label">{label}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("### ✨ Core features")
    cols = st.columns(4)
    features = [
        ("📸", "AI Waste Scan", "Classify waste from an uploaded image."),
        ("⭐", "EcoScore", "Show a simple environmental score for each category."),
        ("🧬", "Biotechnology", "Connect suitable organic waste with biological pathways."),
        ("🏫", "Campus Intelligence", "Track waste patterns by location and college."),
    ]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(
                f'<div class="eco-feature"><div class="eco-feature-icon">{icon}</div>'
                f'<div class="eco-feature-title">{title}</div>'
                f'<div class="eco-feature-text">{desc}</div></div>',
                unsafe_allow_html=True,
            )

# ============================================================
# SCAN
# ============================================================

elif page == TEXT[lang]["scan"]:

    st.markdown('<div class="eco-title">📸 Scan Waste</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="eco-subtitle">Upload an image and let EcoScan analyze it.</div>',
        unsafe_allow_html=True,
    )

    if model_error:
        st.error("The AI model could not be loaded. Please make sure ecoscan_improved.keras is in the project folder.")

    left, right = st.columns([1, 1])

    with left:
        st.markdown('<div class="eco-card"><h3>📍 Scan context</h3></div>', unsafe_allow_html=True)

        location = st.selectbox(
            "Scan Location",
            [
                "Personal Scan",
                "Academic Building",
                "Cafeteria",
                "Laboratories",
                "Library",
                "Student Area",
            ],
        )

        college = None
        if location == "Academic Building":
            college = st.selectbox(
                "College",
                [
                    "Faculty of Medicine",
                    "Faculty of Pharmacy",
                    "Faculty of Biotechnology",
                    "Faculty of Physical Therapy",
                ],
            )

        input_mode = st.radio(
            "Input source",
            ["Gallery / Upload", "Camera"],
            horizontal=True,
        )

        if input_mode == "Camera":
            uploaded_file = st.camera_input("Take a photo")
        else:
            uploaded_file = st.file_uploader(
                "Upload waste image",
                type=["jpg", "jpeg", "png", "webp"],
            )

    with right:
        st.markdown('<div class="eco-card"><h3>🔍 Analysis preview</h3></div>', unsafe_allow_html=True)

        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, use_container_width=True)

            if st.button("🧠 Analyze with EcoScan AI", type="primary", use_container_width=True):
                with st.spinner("EcoScan is analyzing the image..."):
                    predictions = predict_waste(image)

                if not predictions:
                    st.error("No prediction was returned. Check the AI model file.")
                else:
                    waste_type, confidence = predictions[0]
                    info = get_waste_info(waste_type)
                    level, icon = confidence_info(confidence)
                    score = info.get("eco_score", 0)
                    action = info.get("action", "Manual Review")

                    st.session_state["last_scan"] = {
                        "image": image,
                        "waste_type": waste_type,
                        "confidence": confidence,
                        "info": info,
                        "predictions": predictions,
                        "location": location,
                        "college": college,
                        "level": level,
                        "score": score,
                        "action": action,
                    }

        else:
            st.markdown("""
            <div class="eco-card" style="text-align:center;padding:55px 20px;">
                <div style="font-size:50px;">📷</div>
                <h3>Ready to scan</h3>
                <p class="small-muted">
                    Upload or capture an image of a waste item.
                </p>
            </div>
            """, unsafe_allow_html=True)

    if "last_scan" in st.session_state:
        result = st.session_state["last_scan"]
        info = result["info"]

        st.markdown("---")
        st.markdown("### 🧠 AI Result")

        st.markdown(
            f"""
            <div class="eco-result">
                <div class="eco-pill">{result["level"]} Confidence</div>
                <div class="eco-result-type">{result["waste_type"]}</div>
                <p class="small-muted">
                    AI confidence: <b>{result["confidence"]:.2f}%</b>
                </p>
                <div class="eco-pill">Recommended: {result["action"]}</div>
                <div class="eco-pill">Category: {info.get("category","Unknown")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns([1, 2])

        with c1:
            st.markdown(
                f"""
                <div class="eco-score">
                    <div class="small-muted">EcoScore</div>
                    <div class="eco-score-number">{result["score"]}/10</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown("#### 🎯 Top predictions")
            for name, conf in result["predictions"]:
                st.progress(min(conf / 100, 1.0), text=f"{name} — {conf:.2f}%")

        st.markdown("### 💡 Smart Recommendation")
        st.markdown(
            f"""
            <div class="eco-card">
                <h3>🗑️ {info.get("action", "Manual Review")}</h3>
                <p>{info.get("disposal", "")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        r1, r2, r3 = st.columns(3)

        with r1:
            st.markdown(
                f'<div class="eco-feature"><div class="eco-feature-icon">💡</div>'
                f'<div class="eco-feature-title">Reuse</div>'
                f'<div class="eco-feature-text">{info.get("reuse","")}</div></div>',
                unsafe_allow_html=True,
            )

        with r2:
            st.markdown(
                f'<div class="eco-feature"><div class="eco-feature-icon">🌍</div>'
                f'<div class="eco-feature-title">Environmental Impact</div>'
                f'<div class="eco-feature-text">{info.get("impact","")}</div></div>',
                unsafe_allow_html=True,
            )

        biotech = get_biotech_info(result["waste_type"])
        with r3:
            st.markdown(
                f'<div class="eco-feature"><div class="eco-feature-icon">🧬</div>'
                f'<div class="eco-feature-title">Biotechnology</div>'
                f'<div class="eco-feature-text">{biotech.get("explanation","")}</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("### 💾 Save analysis")
        eco_points = calculate_eco_points(result["action"], result["score"])

        s1, s2 = st.columns(2)
        with s1:
            if st.button("💾 Save to History", type="primary", use_container_width=True):
                image_path = save_scan_image(result["image"])
                save_analysis(
                    result["waste_type"],
                    result["confidence"],
                    result["action"],
                    result["score"],
                    image_path,
                    result["location"],
                    result["college"],
                    "Yes" if biotech.get("is_organic") else "No",
                    info.get("landfill_risk", "Unknown"),
                )
                st.success(f"Saved successfully • +{eco_points} EcoPoints")
                st.session_state.pop("last_scan", None)

        with s2:
            if st.button("🔄 Scan Another", use_container_width=True):
                st.session_state.pop("last_scan", None)
                st.rerun()

# ============================================================
# AI ASSISTANT
# ============================================================

elif page == TEXT[lang]["assistant"]:

    st.markdown('<div class="eco-title">🤖 EcoScan AI Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="eco-subtitle">Ask about recycling, disposal, reuse, EcoScore, environment or biotechnology.</div>',
        unsafe_allow_html=True,
    )

    examples = [
        "Is plastic recyclable?",
        "How can I reuse cardboard?",
        "What is the environmental impact of food waste?",
        "Can food waste be composted?",
    ]

    st.markdown("### 💬 Try a question")
    ex_cols = st.columns(4)
    for col, example in zip(ex_cols, examples):
        with col:
            if st.button(example, use_container_width=True):
                st.session_state["assistant_question"] = example

    question = st.text_area(
        "Your question",
        value=st.session_state.get("assistant_question", ""),
        height=120,
        placeholder="Ask EcoScan anything about waste...",
    )

    if st.button("🤖 Ask EcoScan", type="primary", use_container_width=True):
        if question.strip():
            with st.spinner("🧠 EcoScan is thinking..."):
                answer = assistant_response(question)

            st.markdown(
                '<div class="eco-chat"><b>🤖 EcoScan Assistant</b></div>',
                unsafe_allow_html=True,
            )
            st.markdown(answer)
        else:
            st.warning("Please enter a question first.")

# ============================================================
# HISTORY
# ============================================================

elif page == TEXT[lang]["history"]:

    st.markdown('<div class="eco-title">📋 Scan History</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="eco-subtitle">Review previous EcoScan analyses.</div>',
        unsafe_allow_html=True,
    )

    history = get_history()

    if not history:
        st.info("No saved analyses yet. Start by scanning a waste item.")
    else:
        df = pd.DataFrame(
            history,
            columns=[
                "ID", "Date", "Waste Type", "Confidence", "Action",
                "EcoScore", "Image", "Location", "College",
                "Biotech Potential", "Environmental Level"
            ],
        )

        f1, f2, f3 = st.columns(3)

        with f1:
            search = st.text_input("🔎 Search", "")
        with f2:
            waste_options = ["All"] + sorted(df["Waste Type"].dropna().unique().tolist())
            waste_filter = st.selectbox("Waste Type", waste_options)
        with f3:
            location_options = ["All"] + sorted(df["Location"].dropna().unique().tolist())
            location_filter = st.selectbox("Location", location_options)

        filtered = df.copy()

        if search.strip():
            mask = (
                filtered["Waste Type"].astype(str).str.contains(search, case=False, na=False)
                | filtered["Location"].astype(str).str.contains(search, case=False, na=False)
                | filtered["College"].astype(str).str.contains(search, case=False, na=False)
            )
            filtered = filtered[mask]

        if waste_filter != "All":
            filtered = filtered[filtered["Waste Type"] == waste_filter]

        if location_filter != "All":
            filtered = filtered[filtered["Location"] == location_filter]

        st.download_button(
            "⬇️ Download History CSV",
            filtered.to_csv(index=False).encode("utf-8"),
            file_name="ecoscan_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.markdown(f"### {len(filtered)} analysis records")

        for _, row in filtered.iterrows():
            with st.container():
                st.markdown('<div class="eco-card">', unsafe_allow_html=True)

                cols = st.columns([1, 2.2, 2.2, 1.2])

                with cols[0]:
                    image_path = row["Image"]
                    if image_path and os.path.exists(str(image_path)):
                        st.image(str(image_path), use_container_width=True)
                    else:
                        st.markdown("♻️")

                with cols[1]:
                    st.markdown(f"### {row['Waste Type']}")
                    st.markdown(f"**Date:** {row['Date']}")
                    st.markdown(f"**Location:** {row['Location']}")
                    if row["College"] and str(row["College"]) != "None":
                        st.markdown(f"**College:** {row['College']}")

                with cols[2]:
                    st.markdown(f"**Confidence:** {float(row['Confidence']):.2f}%")
                    st.markdown(f"**Action:** {row['Action']}")
                    st.markdown(f"**EcoScore:** {row['EcoScore']}/10")
                    st.markdown(f"**Biotechnology:** {row['Biotech Potential']}")
                    st.markdown(f"**Environmental level:** {row['Environmental Level']}")

                with cols[3]:
                    if st.button("🗑️ Delete", key=f"delete_{row['ID']}", use_container_width=True):
                        delete_analysis(int(row["ID"]))
                        st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🧹 Clear All History", use_container_width=True):
            clear_history()
            st.success("History cleared successfully.")
            st.rerun()

# ============================================================
# DASHBOARD
# ============================================================

elif page == TEXT[lang]["dashboard"]:

    st.markdown('<div class="eco-title">📊 EcoScan Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="eco-subtitle">Understand how the prototype is being used and what waste appears most often.</div>',
        unsafe_allow_html=True,
    )

    history = get_history()

    if not history:
        st.info("Dashboard data will appear after saving scan results.")
    else:
        df = pd.DataFrame(
            history,
            columns=[
                "ID", "Date", "Waste Type", "Confidence", "Action",
                "EcoScore", "Image", "Location", "College",
                "Biotech Potential", "Environmental Level"
            ],
        )

        total = len(df)
        recyclable_count = sum(
            bool(get_waste_info(x).get("recyclable", False))
            for x in df["Waste Type"]
        )
        organic_count = sum(
            x in ["Food Organics", "Vegetation"]
            for x in df["Waste Type"]
        )

        avg_conf = df["Confidence"].mean()
        avg_score = df["EcoScore"].mean()
        ecopoints = sum(
            calculate_eco_points(
                row["Action"], int(row["EcoScore"])
            )
            for _, row in df.iterrows()
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📸 Total Analyses", total)
        c2.metric("♻️ Recyclable", f"{safe_percent(recyclable_count,total)}%")
        c3.metric("🌱 Organic", f"{safe_percent(organic_count,total)}%")
        c4.metric("🧠 Avg Confidence", f"{avg_conf:.1f}%")

        c5, c6 = st.columns(2)
        c5.metric("⭐ Average EcoScore", f"{avg_score:.1f}/10")
        c6.metric("🏆 EcoPoints", ecopoints)

        st.markdown("### 🗂️ Waste Distribution")
        distribution = df["Waste Type"].value_counts()
        st.bar_chart(distribution)

        st.markdown("### 📍 Location Distribution")
        locations = df["Location"].fillna("Unknown").value_counts()
        st.bar_chart(locations)

        most_common = distribution.index[0]
        most_count = int(distribution.iloc[0])

        st.markdown(
            f"""
            <div class="eco-card">
                <h3>🔎 Main insight</h3>
                <p>
                    The most detected waste type is <b>{most_common}</b>,
                    appearing in <b>{most_count}</b> saved analysis record(s).
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# CAMPUS MODE
# ============================================================

elif page == TEXT[lang]["campus"]:

    st.markdown('<div class="eco-title">🏫 Campus Mode</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="eco-subtitle">Explore waste patterns across university locations and colleges.</div>',
        unsafe_allow_html=True,
    )

    history = get_history()

    if not history:
        st.info("Campus insights will appear after saving scan results.")
    else:
        df = pd.DataFrame(
            history,
            columns=[
                "ID", "Date", "Waste Type", "Confidence", "Action",
                "EcoScore", "Image", "Location", "College",
                "Biotech Potential", "Environmental Level"
            ],
        )

        selected_location = st.selectbox(
            "Campus Location",
            [
                "All Campus",
                "Academic Building",
                "Cafeteria",
                "Laboratories",
                "Library",
                "Student Area",
            ],
        )

        selected_college = None
        if selected_location == "Academic Building":
            selected_college = st.selectbox(
                "College",
                [
                    "All Colleges",
                    "Faculty of Medicine",
                    "Faculty of Pharmacy",
                    "Faculty of Biotechnology",
                    "Faculty of Physical Therapy",
                ],
            )

        filtered = df.copy()

        if selected_location != "All Campus":
            filtered = filtered[filtered["Location"] == selected_location]

        if selected_college and selected_college != "All Colleges":
            filtered = filtered[filtered["College"] == selected_college]

        total = len(filtered)

        if total == 0:
            st.warning("No saved scans match this campus filter.")
        else:
            distribution = filtered["Waste Type"].value_counts()
            most_common = distribution.index[0]

            c1, c2, c3 = st.columns(3)
            c1.metric("📸 Analyses", total)
            c2.metric("🗂️ Categories Detected", filtered["Waste Type"].nunique())
            c3.metric("🔎 Most Common", most_common)

            st.markdown("### 📊 Waste distribution")
            st.bar_chart(distribution)

            st.markdown(
                f"""
                <div class="eco-card">
                    <h3>🌱 Campus insight</h3>
                    <p>
                        In the selected campus scope, <b>{most_common}</b>
                        is the most frequently detected category.
                        EcoScan can use this type of information to support
                        future waste-management planning.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ============================================================
# ABOUT
# ============================================================

elif page == TEXT[lang]["about"]:

    st.markdown('<div class="eco-title">ℹ️ About EcoScan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="eco-subtitle">AI-Powered Waste Management Assistant</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="eco-hero">
        <div class="eco-kicker">EcoScan Prototype</div>
        <h1>AI + Waste Intelligence</h1>
        <p>
            EcoScan is a university-focused prototype that uses an AI
            deep-learning model to recognize waste categories and combines
            the prediction with structured waste-management knowledge.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="eco-feature">
            <div class="eco-feature-icon">🧠</div>
            <div class="eco-feature-title">AI Model</div>
            <div class="eco-feature-text">
                Production model accuracy: <b>80.62%</b>.
                The model recognizes 9 waste categories.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="eco-feature">
            <div class="eco-feature-icon">🗂️</div>
            <div class="eco-feature-title">Knowledge Base</div>
            <div class="eco-feature-text">
                Provides disposal, reuse, environmental,
                recycling and EcoScore information.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="eco-feature">
            <div class="eco-feature-icon">🏫</div>
            <div class="eco-feature-title">Campus Impact</div>
            <div class="eco-feature-text">
                Stores location and college context to support
                future campus-level waste analysis.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🗂️ Recognized waste categories")
    category_cols = st.columns(3)

    for i, name in enumerate(class_names):
        with category_cols[i % 3]:
            st.markdown(
                f'<div class="eco-card"><span class="eco-pill">{name}</span></div>',
                unsafe_allow_html=True,
            )

    st.markdown("### 🧬 Biotechnology pathway")
    st.markdown("""
    <div class="eco-card">
        <h3>Organic Waste → Biological Treatment</h3>
        <p class="small-muted">
            For suitable organic categories such as Food Organics and
            Vegetation, EcoScan connects waste information with pathways
            such as composting and anaerobic digestion.
        </p>
    </div>
    """, unsafe_allow_html=True)


<style>
.eco-bottom-spacer {height:8px;}
.eco-bottom-note {
    text-align:center;color:#7a8a83;font-size:11px;
    padding:14px 0 2px;border-top:1px solid #dcebe2;
}
</style>

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="eco-bottom-note">
    ♻️ Smart sorting &nbsp;•&nbsp; 🧠 AI &nbsp;•&nbsp; 🌱 Sustainability
</div>
<div class="eco-footer">
    <b>EcoScan</b> — AI-Powered Waste Management Assistant<br>
    Building smarter and more sustainable communities 🌱
</div>
""", unsafe_allow_html=True)

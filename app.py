import streamlit as st
import tensorflow as tf
import pandas as pd
from PIL import Image
import numpy as np
import os
from datetime import datetime

from waste_knowledge import get_waste_info, get_biotech_info
from ai_assistant import assistant_response
from history_manager import (
    init_database,
    save_analysis,
    get_history,
    delete_analysis,
    clear_history
)


# ============================================================
# EcoScan - AI Waste Classification
# ============================================================

st.set_page_config(
    page_title="EcoScan",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ============================================================
# LANGUAGE / TRANSLATION
# ============================================================

TEXT = {

    "English": {

        # Navigation
        "home": "🏠 Home",
        "scan": "📷 Scan",
        "assistant": "🤖 AI Assistant",
        "history": "📋 History",
        "dashboard": "📊 Dashboard",
        "campus": "🏫 Campus Mode",
        "about": "ℹ️ About",

        # General
        "language": "🌐 Language / اللغة",
        "navigation": "Navigation",

        # Home
        "home_subtitle": "AI-Powered Waste Management Assistant",
        "make_every_waste_count": "🌍 Make Every Waste Count",
        "start_scan": "📷 Start Waste Scan",
        "what_ecoscan_can_do": "🚀 What EcoScan Can Do",

        # Scan
        "scan_title": "📷 Scan Waste",
        "scan_subtitle": "Choose an image from your gallery or use your camera.",
        "scan_location": "📍 Scan Location",
        "where_found": "Where was this item found?",
        "select_college": "🏫 Select College",
        "input_method": "Choose input method",
        "gallery": "🖼️ Gallery",
        "camera": "📷 Camera",
        "upload_image": "Upload waste image",
        "take_picture": "Take a picture of the waste item",
        "preview": "🖼️ Preview",
        "analyze": "🔍 Analyze Waste",
        "analyzing": "🧠 EcoScan is analyzing...",
        "ai_result": "🧠 AI Result",
        "top_predictions": "🔎 Top AI Predictions",
        "smart_recommendation": "♻️ Smart Recommendation",
        "category": "Category",
        "recommended_action": "Recommended Action",
        "best_choice": "⭐ BEST CHOICE",
        "disposal_guidance": "🗑️ Disposal Guidance",
        "reuse_idea": "💡 Reuse Idea",
        "environmental_impact": "🌍 Environmental Impact",
        "biotechnology": "🧬 Biotechnology & Organic Waste",
        "organic_detected": "🌱 Organic waste pathway detected.",
        "high_biological": "🌱 High Biological Potential",
        "treatment_pathway": "Treatment Pathway",
        "ecoscore": "⭐ EcoScore",
        "scan_another": "🔄 Scan Another Item",
        "saved_history": "✅ Analysis saved to your history.",
        "manual_verify": "⚠️ Recommendation requires manual verification because AI confidence is low.",

        # History
        "history_title": "📋 History",
        "history_subtitle": "Your previous EcoScan analyses",
        "download_report": "📥 Download EcoScan Report",
        "total_analyses": "📊 Total Analyses",
        "search": "🔎 Search",
        "waste_type": "🗑️ Waste Type",
        "location": "📍 Location",
        "college": "🏫 College",
        "biotech_potential": "🌱 Biotech Potential",
        "ecoscore_filter": "⭐ EcoScore",
        "clear_history": "Clear History",
        "delete": "🗑️ Delete",

        # Dashboard
        "dashboard_title": "📊 Dashboard",
        "dashboard_subtitle": "Waste analysis overview",
        "total_scans": "🔍 Total Scans",
        "recyclable": "♻️ Recyclable %",
        "organic": "🌱 Organic %",
        "avg_confidence": "🧠 Avg Confidence",
        "avg_ecoscore": "⭐ Avg EcoScore",
        "ecopoints": "🌍 EcoPoints",
        "waste_distribution": "📊 Waste Distribution",
        "waste_location": "📍 Waste by Location",
        "most_detected": "🏆 Most Detected Waste",
        "waste_summary": "🗂️ Waste Summary",
        "insight": "💡 EcoScan Insight",

        # Campus
        "campus_title": "🏫 Campus Mode",
        "campus_subtitle": "AI-powered campus waste insights",
        "campus_location": "📍 Campus Location",
        "select_area": "Select campus area",
        "select_college": "🏫 Select College",
        "campus_distribution": "♻️ Campus Waste Distribution",
        "campus_insight": "💡 Campus Insight",
        "management_recommendation": "🎯 Management Recommendation",

        # About
        "about_title": "ℹ️ About EcoScan",
        "about_subtitle": "AI • Sustainability • Biotechnology",
        "what_is_ecoscan": "♻️ What is EcoScan?",
        "artificial_intelligence": "🧠 Artificial Intelligence",
        "supported_categories": "🗑️ Supported Waste Categories",
        "biotechnology_title": "🧬 Biotechnology",
        "campus_impact": "🏫 Campus Impact"
    },

    "العربية": {

        # Navigation
        "home": "🏠 الرئيسية",
        "scan": "📷 فحص المخلفات",
        "assistant": "🤖 المساعد الذكي",
        "history": "📋 السجل",
        "dashboard": "📊 لوحة المعلومات",
        "campus": "🏫 وضع الجامعة",
        "about": "ℹ️ عن EcoScan",

        # General
        "language": "🌐 اللغة / Language",
        "navigation": "التنقل",

        # Home
        "home_subtitle": "مساعد ذكي لإدارة المخلفات",
        "make_every_waste_count": "🌍 اجعل لكل مخلف قيمة",
        "start_scan": "📷 بدء فحص المخلفات",
        "what_ecoscan_can_do": "🚀 ماذا يستطيع EcoScan أن يفعل؟",

        # Scan
        "scan_title": "📷 فحص المخلفات",
        "scan_subtitle": "اختر صورة من المعرض أو استخدم الكاميرا.",
        "scan_location": "📍 مكان الفحص",
        "where_found": "أين تم العثور على هذه المخلفة؟",
        "select_college": "🏫 اختر الكلية",
        "input_method": "اختر طريقة الإدخال",
        "gallery": "🖼️ المعرض",
        "camera": "📷 الكاميرا",
        "upload_image": "ارفع صورة المخلفة",
        "take_picture": "التقط صورة للمخلفة",
        "preview": "🖼️ معاينة الصورة",
        "analyze": "🔍 تحليل المخلفات",
        "analyzing": "🧠 EcoScan يقوم بتحليل الصورة...",
        "ai_result": "🧠 نتيجة الذكاء الاصطناعي",
        "top_predictions": "🔎 أفضل توقعات الذكاء الاصطناعي",
        "smart_recommendation": "♻️ التوصية الذكية",
        "category": "الفئة",
        "recommended_action": "الإجراء الموصى به",
        "best_choice": "⭐ أفضل اختيار",
        "disposal_guidance": "🗑️ إرشادات التخلص",
        "reuse_idea": "💡 فكرة لإعادة الاستخدام",
        "environmental_impact": "🌍 التأثير البيئي",
        "biotechnology": "🧬 التكنولوجيا الحيوية والمخلفات العضوية",
        "organic_detected": "🌱 تم اكتشاف مسار للمخلفات العضوية.",
        "high_biological": "🌱 إمكانات بيولوجية عالية",
        "treatment_pathway": "مسار المعالجة",
        "ecoscore": "⭐ التقييم البيئي",
        "scan_another": "🔄 فحص عنصر آخر",
        "saved_history": "✅ تم حفظ التحليل في السجل.",
        "manual_verify": "⚠️ يوصى بالتحقق يدويًا لأن درجة ثقة الذكاء الاصطناعي منخفضة.",
        

        # History
        "history_title": "📋 السجل",
        "history_subtitle": "التحاليل السابقة في EcoScan",
        "download_report": "📥 تحميل تقرير EcoScan",
        "total_analyses": "📊 إجمالي التحليلات",
        "search": "🔎 بحث",
        "waste_type": "🗑️ نوع المخلف",
        "location": "📍 المكان",
        "college": "🏫 الكلية",
        "biotech_potential": "🌱 الإمكانات الحيوية",
        "ecoscore_filter": "⭐ التقييم البيئي",
        "clear_history": "مسح السجل",
        "delete": "🗑️ حذف",

        # Dashboard
        "dashboard_title": "📊 لوحة المعلومات",
        "dashboard_subtitle": "نظرة عامة على تحليل المخلفات",
        "total_scans": "🔍 إجمالي عمليات الفحص",
        "recyclable": "♻️ نسبة القابلة لإعادة التدوير",
        "organic": "🌱 نسبة المخلفات العضوية",
        "avg_confidence": "🧠 متوسط الثقة",
        "avg_ecoscore": "⭐ متوسط التقييم البيئي",
        "ecopoints": "🌍 النقاط البيئية",
        "waste_distribution": "📊 توزيع المخلفات",
        "waste_location": "📍 المخلفات حسب المكان",
        "most_detected": "🏆 أكثر نوع مخلفات تم اكتشافه",
        "waste_summary": "🗂️ ملخص المخلفات",
        "insight": "💡 تحليل EcoScan",

        # Campus
        "campus_title": "🏫 وضع الجامعة",
        "campus_subtitle": "رؤى ذكية حول مخلفات الجامعة",
        "campus_location": "📍 موقع الحرم الجامعي",
        "select_area": "اختر منطقة الجامعة",
        "select_college": "🏫 اختر الكلية",
        "campus_distribution": "♻️ توزيع مخلفات الجامعة",
        "campus_insight": "💡 تحليل مخلفات الجامعة",
        "management_recommendation": "🎯 توصية إدارية",

        # About
        "about_title": "ℹ️ عن EcoScan",
        "about_subtitle": "الذكاء الاصطناعي • الاستدامة • التكنولوجيا الحيوية",
        "what_is_ecoscan": "♻️ ما هو EcoScan؟",
        "artificial_intelligence": "🧠 الذكاء الاصطناعي",
        "supported_categories": "🗑️ أنواع المخلفات المدعومة",
        "biotechnology_title": "🧬 التكنولوجيا الحيوية",
        "campus_impact": "🏫 تأثير النظام داخل الجامعة"
    }
}

# ============================================================
# PROFESSIONAL ECO UI
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #f7faf8;
    }

    /* Main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #eef7f1;
        border-right: 1px solid #d8eadf;
    }

    section[data-testid="stSidebar"] h1 {
        color: #126b3f;
    }

    /* Main title */
    .eco-title {
        font-size: 48px;
        font-weight: 800;
        color: #126b3f;
        text-align: center;
        margin-bottom: 0;
    }

    .eco-subtitle {
        text-align: center;
        font-size: 18px;
        color: #527060;
        margin-bottom: 30px;
    }

    /* Cards */
    .eco-card {
        background: #ffffff;
        border: 1px solid #dcebe2;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 4px 15px rgba(30, 80, 50, 0.05);
    }

    .eco-card-green {
        background: #f0f9f3;
        border: 1px solid #cde7d6;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
    }

    .eco-card-title {
        font-size: 22px;
        font-weight: 750;
        color: #126b3f;
        margin-bottom: 10px;
    }

    /* KPI */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #dcebe2;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        min-height: 130px;
    }

    .kpi-icon {
        font-size: 30px;
    }

    .kpi-number {
        font-size: 30px;
        font-weight: 800;
        color: #126b3f;
    }

    .kpi-label {
        color: #61756a;
        font-size: 14px;
    }

    /* Result */
    .result-name {
        font-size: 34px;
        font-weight: 800;
        color: #126b3f;
    }

    .confidence-number {
        font-size: 30px;
        font-weight: 800;
        color: #126b3f;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 30px;
        font-weight: 700;
        margin-top: 5px;
    }

    .badge-green {
        background: #dff3e6;
        color: #126b3f;
    }

    .badge-yellow {
        background: #fff4cf;
        color: #795f00;
    }

    .badge-red {
        background: #fde4e4;
        color: #9d2424;
    }

    /* Footer */
    .eco-footer {
        text-align: center;
        color: #6c8074;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #dcebe2;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE
# ============================================================

init_database()


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("ecoscan_improved.keras")


model = load_model()


# ============================================================
# LOAD CLASS NAMES
# ============================================================

with open("class_names.txt", "r", encoding="utf-8") as file:
    class_names = [line.strip() for line in file.readlines()]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def predict_waste(input_image):

    image_resized = input_image.resize((224, 224))

    image_array = np.array(image_resized)

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    predictions = model.predict(
        image_array,
        verbose=0
    )[0]

    top_indices = np.argsort(
        predictions
    )[-3:][::-1]

    results = []

    for class_index in top_indices:

        predicted_class = class_names[class_index]

        display_name = predicted_class.split(
            "-",
            1
        )[-1]

        confidence = float(
            predictions[class_index]
        ) * 100

        results.append({
            "class": display_name,
            "confidence": confidence
        })

    return results


def get_confidence_info(confidence):

    if confidence >= 80:

        return {
            "level": "High Confidence",
            "emoji": "🟢",
            "class": "badge-green",
            "message": (
                "EcoScan is highly confident in this prediction."
            )
        }

    elif confidence >= 60:

        return {
            "level": "Medium Confidence",
            "emoji": "🟡",
            "class": "badge-yellow",
            "message": (
                "The prediction has moderate confidence. "
                "Please verify the item before disposal."
            )
        }

    else:

        return {
            "level": "Low Confidence",
            "emoji": "🔴",
            "class": "badge-red",
            "message": (
                "EcoScan is not sufficiently confident. "
                "Please verify the item manually."
            )
        }


def get_eco_score_message(score):

    if score >= 9:
        return "Excellent environmental choice 🌍"

    elif score >= 7:
        return "Good environmental option 🌱"

    elif score >= 5:
        return "Moderate environmental benefit ♻️"

    else:
        return "Consider better disposal or reuse options."


def save_scan_image(image):

    os.makedirs(
        "scan_images",
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    image_path = os.path.join(
        "scan_images",
        f"scan_{timestamp}.jpg"
    )

    image.save(
        image_path,
        format="JPEG",
        quality=90
    )

    return image_path

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown(
        "<h1>♻️ EcoScan</h1>",
        unsafe_allow_html=True
    )

    st.caption(
        "AI-Powered Waste Management Assistant"
    )

    # 🌐 Language
    language = st.selectbox(
        "🌐 Language / اللغة",
        ["English", "العربية"]
    )

    st.markdown("---")

    # Navigation
    page_label = st.radio(
        "Navigation",
        [
            TEXT[language]["home"],
            TEXT[language]["scan"],
            TEXT[language]["assistant"],
            TEXT[language]["history"],
            TEXT[language]["dashboard"],
            TEXT[language]["campus"],
            TEXT[language]["about"]
        ],
        label_visibility="collapsed"
    )

    # Keep internal page names unchanged.
    # This prevents breaking the existing page logic.

    page_map = {
        TEXT[language]["home"]: "🏠 Home",
        TEXT[language]["scan"]: "📷 Scan",
        TEXT[language]["assistant"]: "🤖 AI Assistant",
        TEXT[language]["history"]: "📋 History",
        TEXT[language]["dashboard"]: "📊 Dashboard",
        TEXT[language]["campus"]: "🏫 Campus Mode",
        TEXT[language]["about"]: "ℹ️ About"
    }

    page = page_map[page_label]

    st.markdown("---")

    st.markdown(
        """
        **EcoScan AI**

        🧠 AI Classification  
        ♻️ Smart Sorting  
        🌱 Sustainability  
        🧬 Biotechnology
        """
    )

# ============================================================
# HOME
# ============================================================

if page == "🏠 Home":

    st.markdown(
        '<div class="eco-title">♻️ EcoScan</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="eco-subtitle">'
        'AI-Powered Waste Management Assistant'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="eco-card-green">

        <div class="eco-card-title">
        🌍 Make Every Waste Count
        </div>

        EcoScan uses Artificial Intelligence to identify
        waste categories and provide responsible disposal,
        recycling, reuse, and sustainability guidance.

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-icon">🧠</div>
                <div class="kpi-number">80.62%</div>
                <div class="kpi-label">AI Model Accuracy</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-icon">🗑️</div>
                <div class="kpi-number">9</div>
                <div class="kpi-label">Waste Categories</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-icon">🌱</div>
                <div class="kpi-number">Eco</div>
                <div class="kpi-label">Sustainability Focus</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")

    if st.button(
        "📷 Start Waste Scan",
        use_container_width=True
    ):

        st.info(
            "Choose **📷 Scan** from the sidebar to start."
        )

    st.markdown(
        """
        <div class="eco-card">

        <div class="eco-card-title">
        🚀 What EcoScan Can Do
        </div>

        • 🧠 Identify waste using AI<br>
        • ♻️ Recommend responsible disposal<br>
        • ⭐ Calculate an EcoScore<br>
        • 🧬 Explain biological treatment pathways<br>
        • 📋 Keep an analysis history<br>
        • 📊 Analyze waste patterns<br>
        • 🏫 Support campus waste management

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SCAN
# ============================================================
elif page == "📷 Scan":

    st.markdown(
        f'<div class="eco-title">{TEXT[language]["scan_title"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="eco-subtitle">'
        f'{TEXT[language]["scan_subtitle"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.markdown(
            f"### {TEXT[language]['scan_location']}"
        )

        location = st.selectbox(
            TEXT[language]["where_found"],
            [
                "Personal Scan",
                "Academic Building",
                "Cafeteria",
                "Laboratories",
                "Library",
                "Student Area"
            ]
        )

    # 🏫 College Selection
    college = None

    if location == "Academic Building":

        college = st.selectbox(
            TEXT[language]["select_college"],
            [
                "College of Human Medicine",
                "College of Pharmacy",
                "College of Biotechnology",
                "College of Physical Therapy"
            ]
        )

    # --------------------------------------------------------
    # Input method
    # --------------------------------------------------------

    input_method = st.radio(
        TEXT[language]["input_method"],
        [
            TEXT[language]["gallery"],
            TEXT[language]["camera"]
        ],
        horizontal=True
    )

    image = None

    # --------------------------------------------------------
    # Gallery
    # --------------------------------------------------------

    if input_method == TEXT[language]["gallery"]:

        uploaded_file = st.file_uploader(
            TEXT[language]["upload_image"],
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ]
        )

        if uploaded_file is not None:

            image = Image.open(
                uploaded_file
            ).convert("RGB")

    # --------------------------------------------------------
    # Camera
    # --------------------------------------------------------

    else:

        camera_image = st.camera_input(
            TEXT[language]["take_picture"]
        )

        if camera_image is not None:

            image = Image.open(
                camera_image
            ).convert("RGB")

    # --------------------------------------------------------
    # Image Preview
    # --------------------------------------------------------

    if image is not None:

        st.markdown(
            f"### {TEXT[language]['preview']}"
        )

        st.image(
            image,
            use_container_width=True
        )

        st.markdown("")

        analyze_button = st.button(
            TEXT[language]["analyze"],
            use_container_width=True
        )
        if analyze_button:

            with st.spinner(
                TEXT[language] ['analyzing']
            ):

                top_predictions = predict_waste(image)

                predicted_class = top_predictions[0]["class"]

                confidence = top_predictions[0]["confidence"]

                confidence_info = get_confidence_info(
                    confidence
                )

                waste_info = get_waste_info(
                    predicted_class
                )

                biotech_info = get_biotech_info(
                    predicted_class
                )

            # =================================================
            # RESULT CARD
            # =================================================

            st.markdown(
                f"""
                <div class="eco-card">

                <div class="eco-card-title">
                  {TEXT[language]['ai_result']}"
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="result-name">
                {predicted_class}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="confidence-number">
                {confidence:.2f}%
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                min(confidence / 100, 1.0)
            )

            st.markdown(
                f"""
                <div class="badge {confidence_info['class']}">
                {confidence_info['emoji']}
                {confidence_info['level']}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(
                confidence_info["message"]
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"### {TEXT[language]['top_predictions']}"
            )

            for index, prediction in enumerate(top_predictions):

                rank = index + 1

                st.write(
                    f"**#{rank} {prediction['class']}** "
                    f"— {prediction['confidence']:.2f}%"
                )

                st.progress(
                    min(
                        prediction["confidence"] / 100,
                        1.0
                    )
                )

            # =================================================
            # RECOMMENDATION
            # =================================================

            st.markdown(
                f"""
                <div class="eco-card-green">

                <div class="eco-card-title">
                 {TEXT[language]
                 ["smart_recommendation"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(
                f"**{ TEXT[language]['category']}:** {waste_info['category']}"
            )

            st.write(
                f"**{ TEXT[language]['recommended_action']}:** "
                f"{waste_info['action']}"
            )

            if confidence >= 60:

                st.success(
                    f"{ TEXT[language]['best_choice']} — "
                    f"{waste_info['action']}"
                )

            else:
                st.warning(
                  f"{TEXT[language]['manual_verify']} because AI confidence is low."
              )

                

            st.info(
                f"🗑️ **Disposal Guidance:** "
                f"{waste_info['disposal']}"
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

            # =================================================
            # REUSE
            # =================================================

            with st.container(border=True):

                st.markdown(
                    f"### {TEXT[language]['reuse_idea']}"
                 )

                st.write(
                    waste_info["reuse"]
                )

            # =================================================
            # ENVIRONMENTAL IMPACT
            # =================================================

            with st.container(border=True):

                st.markdown(
                    f"### { TEXT[language]['environmental_impact']}"
                )

                st.write(
                    waste_info["impact"]
                )

            # =================================================
            # BIOTECHNOLOGY
            # =================================================

            with st.container(border=True):

                st.markdown(
                    f"### {TEXT[language]['biotechnology']}"
                )

                if biotech_info["is_organic"]:

                    st.success(
                         TEXT[language]["organic_detected"]
                    )

                    st.markdown(
                        f"""
                        <div class="eco-card-green">

                            <div class="eco-card-title">
                                {TEXT[language]["high_biological"]}
                            </div>

                            This waste can potentially be treated
                            through biological processes and converted
                            into useful organic matter.

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.write(
                        f"**{ TEXT[language]['Treatment Pathway']}:** "
                        f"{biotech_info['process']}"
                    )

                    st.info(
                        biotech_info["explanation"]
                    )

                else:

                    st.write(
                        biotech_info["explanation"]
                    )

            # =================================================
            # ECOSCORE
            # =================================================

            with st.container(border=True):

                st.markdown(
                    f"###{TEXT[language]['EcoScore']}"
                )

                score = waste_info["eco_score"]

                st.markdown(
                    f"""
                    <div class="confidence-number">
                    {score}/10
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.progress(
                    score / 10
                )

                st.write(
                    get_eco_score_message(score)
                )

            # =================================================
            # SAVE
            # =================================================

            image_path = save_scan_image(image)

            save_analysis(
              waste_type=predicted_class,
              confidence=confidence,
              action=waste_info["action"],
              eco_score=score,
              image_path=image_path,
              location=location,
              college=college,
              biotech_potential=(
                "High"
                if biotech_info["is_organic"]
                else "Low"
          ),
          environmental_level=(
                "High Positive Impact"
                 if score >= 9
                else "Moderate Positive Impact"
                 if score >= 7
                else "Low Positive Impact"
          )
)

            st.success(
                 TEXT[language]["✅ Analysis saved to your history."]
            )

            # =================================================
            # RESET
            # =================================================

            st.markdown("")

            if st.button(
                TEXT[language][ "🔄 Scan Another Item"],
                use_container_width=True
            ):

                st.rerun()


# ============================================================
# AI ASSISTANT
# ============================================================

elif page == "🤖 AI Assistant":

    st.markdown(
        '<div class="eco-title">🤖 EcoScan AI Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="eco-subtitle">'
        'Ask about waste, recycling, reuse, disposal, EcoScore, '
        'environmental impact, or biotechnology.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="eco-card-green">

        <div class="eco-card-title">
        💬 Ask EcoScan
        </div>

        You can ask your question in <b>Arabic</b> or
        <b>English</b>.

        <br><br>

        Examples:
        <br>
        ♻️ هل البلاستيك قابل لإعادة التدوير؟
        <br>
        🗑️ كيف أتخلص من بقايا الطعام؟
        <br>
        💡 How can I reuse cardboard?
        <br>
        🌍 What is the environmental impact of glass?
        <br>
        🧬 Can food waste be composted?

        </div>
        """,
        unsafe_allow_html=True
    )

    question = st.text_area(
        "💬 Your Question / سؤالك",
        placeholder=(
            "اكتب سؤالك بالعربي أو الإنجليزي...\n"
            "Ask your question in Arabic or English..."
        ),
        height=120
    )

    if st.button(
        "🤖 Ask EcoScan",
        use_container_width=True
    ):

        if question.strip():

            with st.spinner(
                "🧠 EcoScan is thinking..."
            ):

                answer = assistant_response(
                    question
                )

            st.markdown(
                """
                <div class="eco-card">

                <div class="eco-card-title">
                🤖 EcoScan Answer
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(answer)

        else:

            st.warning(
                "⚠️ Please enter a question first."
            )


# ============================================================
# HISTORY
# ============================================================

elif page == "📋 History":

    st.markdown(
        '<div class="eco-title">📋 History</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="eco-subtitle">'
        'Your previous EcoScan analyses'
        '</div>',
        unsafe_allow_html=True
    )

    history = get_history()

    if history:

        data = []

        for record in history:

            data.append({
                "ID": record[0],
                "Date": record[1],
                "Waste Type": record[2],
                "Confidence": record[3],
                "Action": record[4],
                "EcoScore": record[5],
                "Image": record[6],
                "Location": record[7],
                "College": record[8],
                "Biotech Potential": record[9],
                "Environmental Level": record[10]
            })

        df = pd.DataFrame(data)

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📥 Download EcoScan Report",
            csv,
            "ecoscan_report.csv",
            "text/csv",
            use_container_width=True
        )

        st.markdown("---")

    if not history:

        st.info(
            "No analyses recorded yet. Start scanning waste!"
        )

    else:

        st.markdown(
            f"""
            <div class="eco-card-green">
            <div class="eco-card-title">
            📊 Total Analyses
            </div>
            <div class="result-name">
            {len(history)}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("clear history"):

            st.caption(
                "تنبيه: هذا الإجراء سيقوم بحذف جميع التحليلات "
                "المخزنة نهائياً."
            )

            if st.button(
                label="⚠️ Clear All History",
                key="clear_all_btn"
            ):

                clear_history()

                st.toast(
                    "All history has been cleared.",
                    icon="✅"
                )

                st.rerun()

        # ----------------------------------------------------
        # Search
        # ----------------------------------------------------

        search = st.text_input(
            label="🔎 Search",
            placeholder="Search by waste type or location..."
        )

        # ----------------------------------------------------
        # Filters
        # ----------------------------------------------------

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        with col1:

            waste_filter = st.selectbox(
                "🗑️ Waste Type",
                ["All"] + sorted(
                    list(
                        set(
                            record[2]
                            for record in history
                            if len(record) > 2 and record[2]
                        )
                    )
                )
            )

        with col2:

            location_filter = st.selectbox(
                "📍 Location",
                ["All"] + sorted(
                    list(
                        set(
                            record[7]
                            for record in history
                            if len(record) > 7 and record[7]
                        )
                    )
                )
            )

        with col3:

            biotech_filter = st.selectbox(
                "🌱 Biotech Potential",
                ["All"] + sorted(
                    list(
                        set(
                            record[8]
                            for record in history
                            if len(record) > 8 and record[8]
                        )
                    )
                )
            )

        with col4:

            ecoscore_filter = st.selectbox(
                "⭐ EcoScore",
                ["All"] + sorted(
                    list(
                        set(
                            str(record[5])
                            for record in history
                            if len(record) > 5
                            and record[5] is not None
                        )
                    )
                )
            )

        # ----------------------------------------------------
        # Filtering Logic
        # ----------------------------------------------------

        filtered_history = []

        for record in history:

            match_search = (
                not search
            ) or (
                search.lower() in str(record[2]).lower()
                or (
                    len(record) > 7
                    and search.lower()
                    in str(record[7]).lower()
                )
            )

            match_waste = (
                waste_filter == "All"
            ) or (
                len(record) > 2
                and record[2] == waste_filter
            )

            match_location = (
                location_filter == "All"
            ) or (
                len(record) > 7
                and record[7] == location_filter
            )

            match_biotech = (
                biotech_filter == "All"
            ) or (
                len(record) > 8
                and record[8] == biotech_filter
            )

            match_ecoscore = (
                ecoscore_filter == "All"
            ) or (
                len(record) > 5
                and str(record[5]) == ecoscore_filter
            )

            if (
                match_search
                and match_waste
                and match_location
                and match_biotech
                and match_ecoscore
            ):

                filtered_history.append(record)

        st.markdown("---")

        if not filtered_history:

            st.warning(
                "No matching analyses found."
            )

        for record in filtered_history:

            analysis_id = record[0]
            timestamp = record[1]
            waste_type = record[2]
            confidence = record[3]
            action = record[4]
            eco_score = record[5]
            image_path = record[6]
            location = record[7]
            college = record[8]
            biotech_potential = record[9]
            environmental_level = record[10]

            with st.container(border=True):

                col1, col2 = st.columns([1, 2])

                with col1:

                    if (
                        image_path
                        and os.path.exists(image_path)
                    ):

                        st.image(
                            image_path,
                            use_container_width=True
                        )

                with col2:

                    st.markdown(
                        f"### #{analysis_id} — {waste_type}"
                    )

                    st.write(
                        f"🕒 **Date:** {timestamp}"
                    )

                    st.write(
                        f"🧠 **Confidence:** "
                        f"{confidence:.2f}%"
                    )

                    st.write(
                        f"♻️ **Action:** {action}"
                    )

                    st.write(
                        f"⭐ **EcoScore:** "
                        f"{eco_score}/10"
                    )

                    st.write(
                        f"📍 **Location:** {location}"
                    )
                    if college:

                      st.write(
                        f"🏫 **College:** {college}"
                    ) 
                    
                    st.write(
                        f"🧬 **Biotech Potential:** "
                        f"{biotech_potential}"
                    )

                    st.write(
                        f"🌍 **Environmental Impact:** "
                        f"{environmental_level}"
                    )

                    with st.expander("Options"):

                        if st.button(
                            "🗑️ Delete",
                            key=f"delete_{analysis_id}"
                        ):

                            delete_analysis(
                                analysis_id
                            )

                            st.success(
                                "Analysis deleted successfully."
                            )

                            st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

elif page == "📊 Dashboard":

    st.markdown(
        '<div class="eco-title">📊 Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="eco-subtitle">'
        'Waste analysis overview'
        '</div>',
        unsafe_allow_html=True
    )

    history = get_history()

    if not history:

        st.info(
            "Analyze some waste items first to populate the dashboard."
        )

    else:

        total_analyses = len(history)

        waste_counts = {}

        recyclable_count = 0

        organic_count = 0

        total_confidence = 0

        total_ecoscore = 0

        total_ecopoints = 0

        loc_records = []

        for record in history:

            waste_type = record[2]

            confidence = record[3]

            location = (
                record[7]
                if len(record) > 7 and record[7]
                else "Main Campus"
            )

            waste_counts[waste_type] = (
                waste_counts.get(
                    waste_type,
                    0
                ) + 1
            )

            total_confidence += confidence

            waste_info = get_waste_info(
                waste_type
            )

            if waste_info.get(
                "recyclable",
                False
            ):

                recyclable_count += 1

            if waste_type.lower() in [
                "food organics",
                "vegetation"
            ]:

                organic_count += 1

            eco_score = waste_info.get(
                "eco_score",
                5
            )

            action = waste_info.get(
                "action",
                ""
            )

            total_ecoscore += eco_score

            if action == "Recycle":

                action_pts = 10

            elif action == "Compost":

                action_pts = 12

            elif "Reuse" in action:

                action_pts = 8

            else:

                action_pts = 5

            total_ecopoints += (
                action_pts + eco_score
            )

            loc_records.append(
                {
                    "Location": location,
                    "Waste Type": waste_type
                }
            )

        # ----------------------------------------------------
        # Statistical Calculations
        # ----------------------------------------------------

        recyclable_percentage = (
            recyclable_count /
            total_analyses
        ) * 100

        organic_percentage = (
            organic_count /
            total_analyses
        ) * 100

        average_confidence = (
            total_confidence /
            total_analyses
        )

        if average_confidence <= 1.0:

            average_confidence *= 100

        average_ecoscore = (
            total_ecoscore /
            total_analyses
        )

        # ----------------------------------------------------
        # KPI Cards
        # ----------------------------------------------------

        st.markdown(
            "### 📈 Key Performance Indicators (KPIs)"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "🔍 Total Scans",
            f"{total_analyses}"
        )

        col2.metric(
            "♻️ Recyclable %",
            f"{recyclable_percentage:.1f}%"
        )

        col3.metric(
            "🌱 Organic %",
            f"{organic_percentage:.1f}%"
        )

        col4, col5, col6 = st.columns(3)

        col4.metric(
            "🧠 Avg Confidence",
            f"{average_confidence:.1f}%"
        )

        col5.metric(
            "⭐ Avg EcoScore",
            f"{average_ecoscore:.1f} / 10"
        )

        col6.metric(
            "🌍 EcoPoints",
            f"{int(total_ecopoints)} pts"
        )

        st.markdown("---")

        # ----------------------------------------------------
        # Waste Distribution
        # ----------------------------------------------------

        st.markdown(
            "### 📊 Waste Distribution"
        )

        df_counts = pd.DataFrame(
            list(waste_counts.items()),
            columns=[
                "Waste Type",
                "Count"
            ]
        ).set_index(
            "Waste Type"
        )

        st.bar_chart(
            df_counts
        )

        st.markdown("---")

        # ----------------------------------------------------
        # Waste by Location
        # ----------------------------------------------------

        st.markdown(
            "### 📍 Waste by Location"
        )

        df_loc = pd.DataFrame(
            loc_records
        )

        if not df_loc.empty:

            pivot_df = (
                df_loc
                .groupby(
                    [
                        "Location",
                        "Waste Type"
                    ]
                )
                .size()
                .unstack(
                    fill_value=0
                )
            )

            st.bar_chart(
                pivot_df
            )

            with st.expander(
                "📑 View Breakdown Numbers by Location"
            ):

                st.dataframe(
                    pivot_df,
                    use_container_width=True
                )

        # =====================================================
        # KPI CARDS
        # =====================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">🔍</div>
                    <div class="kpi-number">
                    {total_analyses}
                    </div>
                    <div class="kpi-label">
                    Total Analyses
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">♻️</div>
                    <div class="kpi-number">
                    {recyclable_percentage:.1f}%
                    </div>
                    <div class="kpi-label">
                    Potentially Recyclable
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">🌱</div>
                    <div class="kpi-number">
                    {organic_percentage:.1f}%
                    </div>
                    <div class="kpi-label">
                    Organic Waste
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">🧠</div>
                    <div class="kpi-number">
                    {average_confidence:.1f}%
                    </div>
                    <div class="kpi-label">
                    Avg. Confidence
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("")

        # =====================================================
        # MOST DETECTED
        # =====================================================

        most_detected = (
            max(
                waste_counts,
                key=waste_counts.get
            )
            if waste_counts
            else "N/A"
        )

        with st.container(border=True):

            st.markdown(
                "### 🏆 Most Detected Waste"
            )

            st.markdown(
                f"""
                <div class="result-name">
                {most_detected}
                </div>
                """,
                unsafe_allow_html=True
            )

        # =====================================================
        # DISTRIBUTION
        # =====================================================

        with st.container(border=True):

            st.markdown(
                "### 📈 Waste Distribution"
            )

            st.bar_chart(
                waste_counts
            )

        # =====================================================
        # SUMMARY
        # =====================================================

        with st.container(border=True):

            st.markdown(
                "### 🗂️ Waste Summary"
            )

            for waste_type, count in sorted(
                waste_counts.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                percentage = (
                    count /
                    total_analyses
                ) * 100

                st.write(
                    f"**{waste_type}** — "
                    f"{count} analyses "
                    f"({percentage:.1f}%)"
                )

        # =====================================================
        # INSIGHT
        # =====================================================

        with st.container(border=True):

            st.markdown(
                "### 💡 EcoScan Insight"
            )

            st.info(
                f"{most_detected} is currently the "
                f"most frequently detected waste category."
            )

            if recyclable_percentage >= 50:

                st.success(
                    "♻️ More than half of the analyzed "
                    "items were potentially recyclable."
                )

            if organic_percentage > 0:

                st.success(
                    "🌱 Organic waste was detected. "
                    "These materials may be suitable "
                    "for biological treatment such as composting."
                )


# ============================================================
# CAMPUS MODE
# ============================================================

elif page == "🏫 Campus Mode":

    st.markdown(
        '<div class="eco-title">🏫 Campus Mode</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="eco-subtitle">'
        'AI-powered campus waste insights'
        '</div>',
        unsafe_allow_html=True
    )

    history = get_history()

    if not history:

        st.info(
            "Start analyzing waste items to generate campus insights."
        )

    else:

        waste_counts = {}

        for record in history:

            waste_type = record[2]

            waste_counts[waste_type] = (
                waste_counts.get(
                    waste_type,
                    0
                ) + 1
            )

        total = len(history)

        most_common = max(
            waste_counts,
            key=waste_counts.get
        )

        most_common_count = waste_counts[
            most_common
        ]

        most_common_percentage = (
            most_common_count /
            total
        ) * 100

        # =====================================================
        # CAMPUS KPIs
        # =====================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">🔍</div>
                    <div class="kpi-number">
                    {total}
                    </div>
                    <div class="kpi-label">
                    Campus Analyses
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">🗑️</div>
                    <div class="kpi-number">
                    {most_common}
                    </div>
                    <div class="kpi-label">
                    Most Common Waste
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">📊</div>
                    <div class="kpi-number">
                    {most_common_percentage:.1f}%
                    </div>
                    <div class="kpi-label">
                    Category Share
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("")

        # =====================================================
        # LOCATION
        # =====================================================

        with st.container(border=True):

            st.markdown(
                "### 📍 Campus Location"
            )

            campus_location = st.selectbox(
                "Select campus area",
                [
                    "All Campus",
                    "Academic Building",
                    "Cafeteria",
                    "Laboratories",
                    "Library",
                    "Student Area"
                ],
                key="campus_location"
            )

        # =====================================================
        # COLLEGE SELECTION
        # =====================================================

        college = None

        if campus_location == "Academic Building":

            college = st.selectbox(
                "🏫 Select College",
                [
                    "Faculty of Medicine",
                    "Faculty of Pharmacy",
                    "Faculty of Biotechnology",
                    "Faculty of Physical Therapy"
                ],
                key="college_selection"
            )

        st.info(
            f"Currently viewing: **{campus_location}**"
        )

        # =====================================================
        # DISTRIBUTION
        # =====================================================

        with st.container(border=True):

            st.markdown(
                "### ♻️ Campus Waste Distribution"
            )

            st.bar_chart(
                waste_counts
            )

        # =====================================================
        # INSIGHT
        # =====================================================

        with st.container(border=True):

            st.markdown(
                "### 💡 Campus Insight"
            )

            st.info(
                f"{most_common} is currently the most "
                f"frequently detected waste category, "
                f"representing {most_common_percentage:.1f}% "
                f"of recorded analyses."
            )

        # =====================================================
        # RECOMMENDATION
        # =====================================================

        with st.container(border=True):

            st.markdown(
                "### 🎯 Management Recommendation"
            )

            if most_common.lower() == "plastic":

                st.success(
                    "♻️ Increase awareness about plastic "
                    "waste reduction and provide accessible "
                    "recycling collection points."
                )

            elif most_common.lower() in [
                "paper",
                "cardboard"
            ]:

                st.success(
                    "📄 Increase paper recycling points "
                    "and promote digital alternatives."
                )

            elif most_common.lower() in [
                "food organics",
                "vegetation"
            ]:

                st.success(
                    "🌱 Consider dedicated organic waste "
                    "collection and biological treatment."
                )

            elif most_common.lower() == "glass":

                st.success(
                    "🍾 Provide dedicated glass collection "
                    "containers and improve separation."
                )

            elif most_common.lower() == "metal":

                st.success(
                    "🔩 Increase collection capacity "
                    "for recyclable metal waste."
                )

            else:

                st.warning(
                    "⚠️ Review waste composition and improve "
                    "separation and collection practices."
                )


# ============================================================
# ABOUT
# ============================================================

elif page == "ℹ️ About":

    st.markdown(
        '<div class="eco-title">ℹ️ About EcoScan</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="eco-subtitle">'
        'AI • Sustainability • Biotechnology'
        '</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.markdown(
            "### ♻️ What is EcoScan?"
        )

        st.write(
            "EcoScan is an AI-powered waste management "
            "assistant designed to classify waste items "
            "and provide responsible disposal guidance."
        )

    with st.container(border=True):

        st.markdown(
            "### 🧠 Artificial Intelligence"
        )

        st.write(
            "EcoScan uses a deep learning image "
            "classification model trained to recognize "
            "9 waste categories."
        )

        st.write(
            "**Production Model Accuracy:** 80.62%"
        )

    with st.container(border=True):

        st.markdown(
            "### 🗑️ Supported Waste Categories"
        )

        for waste_class in class_names:

            display_class = waste_class.split(
                "-",
                1
            )[-1]

            st.write(
                f"♻️ {display_class}"
            )

    with st.container(border=True):

        st.markdown(
            "### 🧬 Biotechnology"
        )

        st.write(
            "For biodegradable organic waste, EcoScan "
            "introduces an educational pathway involving "
            "biological treatment and composting."
        )

    with st.container(border=True):

        st.markdown(
            "### 🏫 Campus Impact"
        )

        st.write(
            "Campus Mode transforms individual waste "
            "analyses into aggregated insights that "
            "can support better waste-management decisions."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="eco-footer">
        ♻️ <b>EcoScan</b> — AI-Powered Waste Management Assistant<br>
        Building smarter and more sustainable communities 🌱
    </div>
    """,
    unsafe_allow_html=True
)

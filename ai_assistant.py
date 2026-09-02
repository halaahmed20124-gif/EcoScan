# ==========================================
# EcoScan - AI Assistant
# No API / No API Key Required
# ==========================================

import re
from waste_knowledge import WASTE_INFO, get_waste_info


# ==========================================
# Waste name detection
# ==========================================

WASTE_ALIASES = {
    "plastic": [
        "plastic", "بلاستيك", "زجاجة بلاستيك", "عبوة بلاستيك"
    ],
    "paper": [
        "paper", "ورق", "ورقة"
    ],
    "cardboard": [
        "cardboard", "كرتون", "كرتونه", "صندوق كرتون"
    ],
    "glass": [
        "glass", "زجاج", "ازاز", "زجاجة زجاج"
    ],
    "metal": [
        "metal", "معدن", "علبة معدن", "حديد", "الومنيوم", "ألمنيوم"
    ],
    "food organics": [
        "food", "food waste", "food organics",
        "طعام", "بقايا الطعام", "مخلفات الطعام", "اكل", "أكل"
    ],
    "vegetation": [
        "vegetation", "plants", "plant",
        "نبات", "نباتات", "مخلفات نباتية", "ورق شجر", "شجر"
    ],
    "textile trash": [
        "textile", "textiles", "cloth", "clothes",
        "ملابس", "قماش", "منسوجات"
    ],
    "miscellaneous trash": [
        "miscellaneous", "trash", "other waste",
        "قمامة", "مخلفات", "نفايات", "زبالة"
    ]
}


# ==========================================
# Find waste type from question
# ==========================================

def detect_waste(question):

    q = question.lower().strip()

    for waste_type, aliases in WASTE_ALIASES.items():

        for alias in aliases:

            if alias.lower() in q:
                return waste_type

    # Check exact knowledge-base names
    for waste_name in WASTE_INFO:

        if waste_name.lower() in q:
            return waste_name.lower()

    return None


# ==========================================
# Detect user language
# ==========================================

def detect_language(question):

    arabic_chars = re.findall(
        r'[\u0600-\u06FF]',
        question
    )

    if len(arabic_chars) > 2:
        return "ar"

    return "en"


# ==========================================
# Detect question intent
# ==========================================

def detect_intent(question):

    q = question.lower()

    intents = {

        "recycle": [
            "recycle",
            "recyclable",
            "recycling",
            "إعادة تدوير",
            "يتدوّر",
            "قابل للتدوير"
        ],

        "disposal": [
            "dispose",
            "disposal",
            "throw",
            "bin",
            "where should",
            "التخلص",
            "ارمي",
            "أرمي",
            "الرمي",
            "مكان التخلص"
        ],

        "reuse": [
            "reuse",
            "reuse idea",
            "repurpose",
            "إعادة استخدام",
            "استخدمه تاني",
            "استخدام"
        ],

        "impact": [
            "environment",
            "environmental",
            "impact",
            "harm",
            "pollution",
            "بيئة",
            "بيئي",
            "تلوث",
            "ضرر"
        ],

        "score": [
            "score",
            "ecoscore",
            "eco score",
            "points",
            "درجة",
            "التقييم",
            "النقاط"
        ],

        "biotech": [
            "biotechnology",
            "biotech",
            "compost",
            "biological",
            "microorganism",
            "microorganisms",
            "تكنولوجيا حيوية",
            "بايوتكنولوجي",
            "تسميد",
            "كمبوست",
            "تحلل"
        ],

        "category": [
            "category",
            "type",
            "kind",
            "نوع",
            "تصنيف",
            "فئة"
        ]
    }

    for intent, keywords in intents.items():

        for keyword in keywords:

            if keyword in q:
                return intent

    return "general"


# ==========================================
# English response
# ==========================================

def english_response(waste_type, intent):

    # Find actual database key
    actual_name = None

    for name in WASTE_INFO:

        if name.lower() == waste_type.lower():
            actual_name = name
            break

    if actual_name is None:

        for name, aliases in WASTE_ALIASES.items():

            if name == waste_type:
                for db_name in WASTE_INFO:

                    if db_name.lower() == name:
                        actual_name = db_name
                        break

    if actual_name is None:
        return None

    info = get_waste_info(actual_name)

    if intent == "recycle":

        if info["recyclable"]:

            return (
                f"♻️ Yes. {actual_name} is potentially recyclable.\n\n"
                f"Recommended action: {info['action']}.\n\n"
                f"Guidance: {info['disposal']}"
            )

        return (
            f"♻️ {actual_name} is not listed as primarily "
            f"recyclable in the EcoScan knowledge base.\n\n"
            f"Recommended action: {info['action']}.\n\n"
            f"Guidance: {info['disposal']}"
        )

    if intent == "disposal":

        return (
            f"🗑️ For {actual_name}, the recommended action is "
            f"**{info['action']}**.\n\n"
            f"{info['disposal']}"
        )

    if intent == "reuse":

        return (
            f"💡 Reuse idea for {actual_name}:\n\n"
            f"{info['reuse']}"
        )

    if intent == "impact":

        return (
            f"🌍 Environmental impact of {actual_name}:\n\n"
            f"{info['impact']}\n\n"
            f"Landfill risk: {info.get('landfill_risk', 'Not specified')}."
        )

    if intent == "score":

        return (
            f"⭐ EcoScore for {actual_name}: "
            f"{info['eco_score']}/10.\n\n"
            f"{info['impact']}"
        )

    if intent == "biotech":

        if actual_name in ["Food Organics", "Vegetation"]:

            return (
                f"🧬 {actual_name} has biological treatment potential.\n\n"
                f"A suitable pathway is:\n"
                f"Separation → Biological Treatment → "
                f"Composting → Organic Matter Recovery.\n\n"
                f"Recovery method: {info['recovery_method']}"
            )

        return (
            f"🧬 {actual_name} is not primarily biodegradable "
            f"organic waste, so biological treatment is not "
            f"the main recommended pathway.\n\n"
            f"Recovery method: {info['recovery_method']}"
        )

    if intent == "category":

        return (
            f"🗂️ {actual_name} belongs to the category: "
            f"**{info['category']}**."
        )

    # General question
    return (
        f"♻️ Here is what I know about {actual_name}:\n\n"
        f"**Category:** {info['category']}\n\n"
        f"**Recommended action:** {info['action']}\n\n"
        f"**Disposal:** {info['disposal']}\n\n"
        f"**Reuse:** {info['reuse']}\n\n"
        f"**EcoScore:** {info['eco_score']}/10\n\n"
        f"**Environmental impact:** {info['impact']}"
    )


# ==========================================
# Arabic response
# ==========================================

def arabic_response(waste_type, intent):

    # Match database name
    actual_name = None

    for name in WASTE_INFO:

        aliases = WASTE_ALIASES.get(
            name.lower(),
            []
        )

        if name.lower() == waste_type.lower():
            actual_name = name
            break

        if waste_type.lower() in aliases:
            actual_name = name
            break

    if actual_name is None:
        return None

    info = get_waste_info(actual_name)

    if intent == "recycle":

        if info["recyclable"]:

            return (
                f"♻️ نعم، {actual_name} قابل لإعادة التدوير "
                f"بشكل مناسب.\n\n"
                f"الإجراء المقترح: {info['action']}.\n\n"
                f"الإرشادات: {info['disposal']}"
            )

        return (
            f"♻️ {actual_name} ليس من المواد المصنفة "
            f"أساسًا كمواد قابلة لإعادة التدوير في قاعدة EcoScan.\n\n"
            f"الإجراء المقترح: {info['action']}.\n\n"
            f"الإرشادات: {info['disposal']}"
        )

    if intent == "disposal":

        return (
            f"🗑️ بالنسبة إلى {actual_name}، "
            f"الإجراء المقترح هو: **{info['action']}**.\n\n"
            f"{info['disposal']}"
        )

    if intent == "reuse":

        return (
            f"💡 فكرة لإعادة استخدام {actual_name}:\n\n"
            f"{info['reuse']}"
        )

    if intent == "impact":

        return (
            f"🌍 التأثير البيئي لـ {actual_name}:\n\n"
            f"{info['impact']}\n\n"
            f"مخاطر الطمر: "
            f"{info.get('landfill_risk', 'غير محددة')}."
        )

    if intent == "score":

        return (
            f"⭐ درجة EcoScore لـ {actual_name} هي "
            f"{info['eco_score']}/10.\n\n"
            f"{info['impact']}"
        )

    if intent == "biotech":

        if actual_name in ["Food Organics", "Vegetation"]:

            return (
                f"🧬 {actual_name} لديه إمكانية جيدة "
                f"للمعالجة البيولوجية.\n\n"
                f"المسار المقترح:\n"
                f"فصل المخلفات → معالجة بيولوجية → "
                f"Composting → استعادة المادة العضوية.\n\n"
                f"طريقة الاستعادة: {info['recovery_method']}"
            )

        return (
            f"🧬 {actual_name} ليس من المخلفات العضوية "
            f"القابلة للتحلل بشكل أساسي، لذلك المعالجة "
            f"البيولوجية ليست المسار الرئيسي له.\n\n"
            f"طريقة الاستعادة: {info['recovery_method']}"
        )

    if intent == "category":

        return (
            f"🗂️ {actual_name} ينتمي إلى فئة:\n"
            f"**{info['category']}**."
        )

    # General
    return (
        f"♻️ دي المعلومات المتاحة عن {actual_name}:\n\n"
        f"**الفئة:** {info['category']}\n\n"
        f"**الإجراء المقترح:** {info['action']}\n\n"
        f"**طريقة التخلص:** {info['disposal']}\n\n"
        f"**فكرة إعادة الاستخدام:** {info['reuse']}\n\n"
        f"**EcoScore:** {info['eco_score']}/10\n\n"
        f"**التأثير البيئي:** {info['impact']}"
    )


# ==========================================
# Main Assistant
# ==========================================

def assistant_response(question):

    question = question.strip()

    if not question:

        return (
            "👋 Ask me anything about waste, recycling, "
            "reuse, disposal, EcoScore, or biotechnology."
        )

    language = detect_language(question)

    waste_type = detect_waste(question)

    intent = detect_intent(question)

    # --------------------------------------
    # Waste-related question
    # --------------------------------------

    if waste_type:

        if language == "ar":

            response = arabic_response(
                waste_type,
                intent
            )

        else:

            response = english_response(
                waste_type,
                intent
            )

        if response:
            return response

    # --------------------------------------
    # General questions
    # --------------------------------------

    q = question.lower()

    if language == "ar":

        if any(
            word in q
            for word in [
                "ماذا يمكنك",
                "تقدر تعمل ايه",
                "تقدر تعمل إيه",
                "ايه اللي تقدر",
                "مساعد"
            ]
        ):

            return (
                "🤖 أنا EcoScan Assistant.\n\n"
                "أقدر أساعدك في:\n\n"
                "♻️ إعادة التدوير\n"
                "🗑️ طرق التخلص من المخلفات\n"
                "💡 إعادة الاستخدام\n"
                "🌍 التأثير البيئي\n"
                "⭐ EcoScore\n"
                "🧬 التكنولوجيا الحيوية\n"
                "🗂️ تصنيف المخلفات\n\n"
                "مثال:\n"
                "• هل البلاستيك قابل لإعادة التدوير؟\n"
                "• كيف أتخلص من بقايا الطعام؟\n"
                "• ما تأثير الزجاج على البيئة؟\n"
                "• What can I do with cardboard?"
            )

        if "مرحبا" in q or "اهلا" in q or "أهلا" in q:

            return (
                "👋 أهلاً بك في EcoScan Assistant!\n\n"
                "اسألني عن أي نوع من المخلفات "
                "أو عن إعادة التدوير وإعادة الاستخدام "
                "والتأثير البيئي."
            )

        return (
            "🤔 أقدر أساعدك في الأسئلة المتعلقة بالمخلفات "
            "والاستدامة.\n\n"
            "جربي مثلاً:\n"
            "♻️ هل البلاستيك قابل لإعادة التدوير؟\n"
            "🗑️ كيف أتخلص من الورق؟\n"
            "💡 كيف أعيد استخدام الكرتون؟\n"
            "🌍 ما تأثير المخلفات الغذائية؟\n"
            "🧬 هل يمكن عمل Composting؟"
        )

    else:

        if any(
            word in q
            for word in [
                "what can you do",
                "help",
                "who are you"
            ]
        ):

            return (
                "🤖 I am EcoScan Assistant.\n\n"
                "I can help with:\n\n"
                "♻️ Recycling\n"
                "🗑️ Waste disposal\n"
                "💡 Reuse ideas\n"
                "🌍 Environmental impact\n"
                "⭐ EcoScore\n"
                "🧬 Biotechnology\n"
                "🗂️ Waste categories\n\n"
                "Try asking:\n"
                "• Is plastic recyclable?\n"
                "• How should I dispose of food waste?\n"
                "• Give me a reuse idea for cardboard.\n"
                "• What is the environmental impact of glass?"
            )

        if "hello" in q or "hi" in q:

            return (
                "👋 Hello! Welcome to EcoScan Assistant.\n\n"
                "Ask me about waste, recycling, "
                "reuse, disposal, or sustainability."
            )

        return (
            "🤔 I can help with waste-management questions.\n\n"
            "Try asking:\n"
            "♻️ Is plastic recyclable?\n"
            "🗑️ How should I dispose of paper?\n"
            "💡 How can I reuse cardboard?\n"
            "🌍 What is the environmental impact of food waste?\n"
            "🧬 Can food waste be composted?"
        )

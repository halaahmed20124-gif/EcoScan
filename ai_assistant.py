from openai import OpenAI
import streamlit as st


def get_ai_response(
    user_message,
    conversation_history=None,
    scan_context=None
):
    """
    Generate an EcoScan AI Assistant response.

    The assistant focuses on:
    - Waste management
    - Recycling
    - Reuse
    - Sustainability
    - Environmental education
    - Biotechnology related to waste
    - Campus waste solutions
    """

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    system_prompt = """
You are EcoScan AI Assistant, an educational environmental
assistant inside the EcoScan waste-management application.

Your role is to help students and users understand:
- Waste classification
- Recycling
- Reuse
- Responsible disposal
- Sustainability
- Environmental impact
- Organic waste
- Composting
- Biotechnology related to biodegradable waste
- School and campus waste-management solutions

Answer in a clear, friendly and educational way.

Important rules:
1. Give practical and easy-to-understand suggestions.
2. Do not claim that every material is recyclable everywhere.
3. When disposal depends on local rules, clearly say that the user
   should check their local waste-management or recycling rules.
4. For the nine EcoScan categories, use the provided EcoScan
   information as the primary context when available.
5. If a question is unrelated to environmental topics, politely
   explain that you are specialized in EcoScan, environment,
   sustainability and waste-management questions.
6. Never invent a specific local recycling facility or collection
   service.
7. For biotechnology questions, explain concepts educationally
   and safely.
8. Keep answers appropriate for students.
9. If the user asks a follow-up question, use the previous
   conversation context.
"""

    context_text = ""

    if scan_context:
        context_text = f"""
Current EcoScan scan context:

Waste type: {scan_context.get("waste_type", "Unknown")}
Confidence: {scan_context.get("confidence", "Unknown")}
EcoScore: {scan_context.get("eco_score", "Unknown")}/10
Recommended action: {scan_context.get("action", "Unknown")}
Disposal guidance: {scan_context.get("disposal", "Unknown")}
Reuse idea: {scan_context.get("reuse", "Unknown")}
Environmental impact: {scan_context.get("impact", "Unknown")}
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt + context_text
        }
    ]

    if conversation_history:

        for message in conversation_history:

            messages.append(
                {
                    "role": message["role"],
                    "content": message["content"]
                }
            )

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=messages
    )

    return response.output_text

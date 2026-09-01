import streamlit as st
from openai import OpenAI


def get_ai_response(user_question, conversation_history=None, eco_context=""):
    """
    Generate a dynamic AI response for EcoScan.
    """

    if not st.secrets.get("OPENAI_API_KEY"):
        return (
            "⚠️ AI Assistant is not connected yet. "
            "Please add the OpenAI API key in Streamlit Secrets."
        )

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    system_prompt = f"""
You are EcoScan AI Assistant.

EcoScan is an educational AI-powered waste management
application focused on sustainability, recycling,
waste sorting, environmental awareness, and biotechnology.

Your job is to:
- Answer the student's question naturally.
- Generate a new answer based on the question.
- Do NOT use fixed answers.
- Explain difficult ideas in simple language.
- Give practical and environmentally responsible suggestions.
- When relevant, explain recycling, reuse, composting,
  waste separation, environmental impact, and biotechnology.
- If the question is unrelated to EcoScan, you may still
  answer briefly and helpfully.
- Never pretend to know something you do not know.
- If information is uncertain, clearly say so.
- Do not give dangerous instructions.

EcoScan knowledge available to you:

{eco_context}

Answer in the same language used by the student.
If the student asks in Arabic, answer in Arabic.
If the student asks in English, answer in English.
"""

    messages = [
        {
            "role": "developer",
            "content": system_prompt
        }
    ]

    if conversation_history:
        messages.extend(conversation_history)

    messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=messages
        )

        return response.output_text

    except Exception as error:

        return (
            "⚠️ Sorry, I couldn't connect to the AI service.\n\n"
            f"Error: {error}"
        )

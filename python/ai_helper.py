import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from course_data import AI_SYSTEM_PROMPT


def get_mistral_client() -> MistralClient:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY is not set")
    return MistralClient(api_key=api_key)


async def get_ai_response(user_question: str) -> str:
    try:
        client = get_mistral_client()
        messages = [
            ChatMessage(role="system", content=AI_SYSTEM_PROMPT),
            ChatMessage(role="user", content=user_question),
        ]
        response = client.chat(
            model="mistral-small",
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Не удалось получить ответ от AI. Попробуйте позже.\n\nОшибка: {str(e)}"

import ollama
from .LLM_query import build_prompt
from backend.database import SessionLocal
from backend.services.jmdict import search_words_by_translation


async def get_word_from_db(word):
    async with SessionLocal() as db_session:
        data = await search_words_by_translation(db_session, word, limit=1)
    return data[0]


async def generate(translation):
    print("\nГенерация ответа...")
    response = await ollama.AsyncClient().generate(
        model="qwen3:0.6b",
        prompt=(build_prompt(await get_word_from_db(translation))),
        think=False
    )

    print(response["response"])

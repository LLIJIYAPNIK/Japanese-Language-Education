import asyncio
import ollama
import time
from LLM_query import build_prompt

from database import JapanizeCRUD, SessionLocal


async def get_word_from_db(translation):
    db = JapanizeCRUD(SessionLocal)

    word = await db.get_words_by_partial_translation(
        translation, limit=1
    )

    print(word)
    return word[0]


async def main(translation):
    # Генерируем ответ
    start = time.time()
    print("\nГенерация ответа...")
    response = await ollama.AsyncClient().generate(
        model="qwen3:0.6b",  # Твоя модель
        prompt=(build_prompt(await get_word_from_db(translation))),
        think=False
    )

    # Выводим результат
    print("\nОтвет Ollama:")
    print(response["response"])
    end = time.time()
    print(end-start)

if __name__ == "__main__":
    asyncio.run(main("клавиатура"))
import asyncio
import os
import json
from backend.database import SessionLocal
from backend.services.jmdict import add_word_translation_link


async def migrate_to_postgresql():
    """Асинхронно мигрирует данные из JSON в PostgreSQL"""
    total = 0

    try:
        session = SessionLocal()
        # Обрабатываем все файлы в папке
        for file in os.listdir("japan_dict_json"):
            dictionary = json.load(open(os.path.join("japan_dict_json", file), encoding='utf-8'))
            for word in dictionary:
                translation = " ".join(word[5])
                await add_word_translation_link(
                    session=session,
                    kanji=word[0],
                    kana=word[1],
                    translation_text=translation,
                    rating=word[4]
                )
                total += 1
                await session.flush()

        await session.commit()
        print(f"✅ Успешно мигрировано {total} записей в PostgreSQL")

    except Exception as e:
        print(f"❌ Ошибка миграции: {str(e)}")
        raise e


if __name__ == "__main__":
    asyncio.run(migrate_to_postgresql())

import asyncio
import aiohttp
from voicevox import Client

from backend.database import engine, Base, SessionLocal
from backend.services.jmdict.search import search_words_by_translation
from backend.services.jmdict.queries import get_translations_by_word
from config import UNSPLASH_CLIENT_ID, UNSPLASH_REGULAR_IMAGES_DIR, UNSPLASH_SMALL_IMAGES_DIR, TTS_GENERATIONS_DIR
from backend.services.unsplash import UnsplashService
from backend.services.tts import VoicevoxTTSClient

async def create_tables() -> None:
    """
    Создает таблицы в базе данных, если они еще не существуют.

    Использует SQLAlchemy для выполнения команды создания таблиц на основе метаданных модели.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    word = "клавиатура"
    async with SessionLocal() as db_session:
        data = await search_words_by_translation(db_session, word)
        word_ru = await get_translations_by_word(db_session, word)
    print(data)
    print(word_ru)

    async with SessionLocal() as db_session, aiohttp.ClientSession() as http_client:
        unsplash_service = UnsplashService(
            api_key=UNSPLASH_CLIENT_ID,
            regular_dir=UNSPLASH_REGULAR_IMAGES_DIR,
            small_dir=UNSPLASH_SMALL_IMAGES_DIR,
            db_session=db_session,
            http_client=http_client,
            page=10,
            image_number=3
        )
        image_id, regular_url, small_url = await unsplash_service.get_image_data()
        await unsplash_service.save_images(image_id, regular_url, small_url)

    async with Client() as client:
        await VoicevoxTTSClient(TTS_GENERATIONS_DIR, "青峰大樹vs鏡大河inストリーム。進め 誠林！", client).get_audio()


if __name__ == "__main__":
    asyncio.run(main())

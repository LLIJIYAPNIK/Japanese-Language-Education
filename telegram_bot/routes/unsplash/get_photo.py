import aiohttp
from aiogram import Router, types
from aiogram.filters import CommandStart

from main import bot

from config import UNSPLASH_KEY, UNSPLASH_REGULAR_IMAGES_DIR, UNSPLASH_SMALL_IMAGES_DIR

from backend.database import SessionLocal
from backend.services.unsplash import UnsplashService


unsplash_router = Router()

@unsplash_router.message(CommandStart)
async def send_photo(message: types.Message):
    async with SessionLocal() as db_session, aiohttp.ClientSession() as http_client:
        unsplash_service = UnsplashService(
            api_key=UNSPLASH_KEY,
            regular_dir=UNSPLASH_REGULAR_IMAGES_DIR,
            small_dir=UNSPLASH_SMALL_IMAGES_DIR,
            db_session=db_session,
            http_client=http_client,
            page=10,
            image_number=3
        )
        try:
            image_id, regular_url, small_url = await unsplash_service.get_image_data()
            await unsplash_service.save_images(image_id, regular_url, small_url)
            await bot.send_photo(message.chat.id, regular_url)
        except Exception as e:
            await message.answer("Произошла ошибка при попытке отправки изображения...")

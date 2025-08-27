import asyncio
from backend.database import Base
from backend.database import engine
from main import bot, dp
from telegram_bot.routes.unsplash import unsplash_router

async def create_tables() -> None:
    """
    Создает таблицы в базе данных, если они еще не существуют.

    Использует SQLAlchemy для выполнения команды создания таблиц на основе метаданных модели.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main() -> None:
    """
    Основная функция для инициализации и запуска бота.

    Создает таблицы в базе данных, добавляет обработчики в диспетчер и запускает бота.
    Также инициирует периодическое обновление дат.
    """
    # Создание таблиц в базе данных
    await create_tables()

    # Добавление обработчиков в диспетчер
    dp.include_router(unsplash_router)


    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())

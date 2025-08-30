from aiogram import Bot, Router, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from config import TELEGRAM_TOKEN



TOKEN = TELEGRAM_TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

start_router = Router()

@start_router.message(CommandStart())
async def command_start(message: types.Message):
    await message.reply("Hello, yo")

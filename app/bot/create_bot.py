from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

from app.config import settings

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def start_bot():
    try:
        await bot.send_message(settings.ADMIN_ID, f'Бот запущен.')
    except:
        pass


async def stop_bot():
    try:
        await bot.send_message(settings.ADMIN_ID, 'Бот остановлен.')
    except:
        pass

async def delete_prev_messages(message: Message)->None:
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)

async def delete_message(message: Message)-> None:
    await bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)

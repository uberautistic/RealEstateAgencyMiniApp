from aiogram.types import ReplyKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.config import settings


def main_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    url_add_application = f'{settings.BASE_SITE}/home?user_id={user_id}'
    kb.button(text="Открыть приложение", web_app=WebAppInfo(url=url_add_application))
    kb.button(text="Политика конфиденциальности")

    return kb.as_markup(resize_keyboard=True)

def back_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Назад")
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)

def register_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Поделиться номером телефона", request_contact=True)
    kb.button(text="Политика конфиденциальности")
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)

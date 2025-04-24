import logging
import requests
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from app.api.dao import UserDAO
from app.bot.kbs import register_keyboard, back_keyboard
from app.bot.utils import greet_user, get_policy_text
from app.config import settings
from app.bot.create_bot import delete_prev_messages, delete_message

user_router = Router()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Form(StatesGroup):
    waiting_for_phone = State()


@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    user = await UserDAO.find_one_or_none(telegram_id=message.from_user.id)
    if not user:
        await state.set_state(Form.waiting_for_phone)
        await message.answer(f'{message.from_user.first_name}, Здравствуйте! '
                             f'Для завершения регистрации поделитесь своим номером телефона.\n'
                             f'Предоставляя свой номер телефона вы соглашаетесь с политикой конфиденциальности.',
                             reply_markup=register_keyboard())
    else:
        await greet_user(message,
                         is_new_user=not user,
                         phone_number=user.phone_number)

    await delete_message(message)


@user_router.message(F.contact)
async def process_contact(message: Message, state: FSMContext):
    user = await UserDAO.find_one_or_none(telegram_id=message.from_user.id)

    if not user:
        await UserDAO.add(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            username=message.from_user.username,
            phone_number=message.contact.phone_number
        )
        await greet_user(message,
                         is_new_user=True,
                         phone_number=message.contact.phone_number)
        await state.set_state(None)
        try:
            url = f'{settings.INFOBASE_SITE}/telegram/clients/'
            headers = {'Content-Type': 'application/json'}
            data = {
                'telegram_id': message.from_user.id,
                'first_name': message.from_user.first_name,
                'username': message.from_user.username,
                'phone_number': message.contact.phone_number
            }
            response = requests.post(url, headers=headers, json=data)
            logging.info(response.json()['response'])

        except Exception as e:
            logging.error(f'Ошибка: {e}')

        await delete_prev_messages(message)


@user_router.message(F.text == 'Назад')
async def cmd_back(message: Message, state: FSMContext) -> None:
    user = await UserDAO.find_one_or_none(telegram_id=message.from_user.id)
    if not user:
        await state.set_state(Form.waiting_for_phone)
        await message.answer(f'Для завершения регистрации поделитесь своим номером телефона.'
                             f'Предоставляя свой номер телефона вы соглашаетесь с политикой конфиденциальности.',
                             reply_markup=register_keyboard())
    else:
        await greet_user(message,
                         is_new_user=not user,
                         phone_number=user.phone_number)
    await delete_prev_messages(message)


@user_router.message(F.text == "Политика конфиденциальности")
async def policy(message: Message):
    kb = back_keyboard()
    await message.answer(get_policy_text(),reply_markup=kb)
    await delete_prev_messages(message)



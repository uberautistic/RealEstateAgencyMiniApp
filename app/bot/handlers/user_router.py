from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from app.api.dao import UserDAO
from app.bot.keyboards.kbs import app_keyboard, register_keyboard
from app.bot.utils.utils import greet_user, get_about_us_text

user_router = Router()

class Form(StatesGroup):
    waiting_for_phone = State()

@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    # регистрация без номера телефона
    # user = await UserDAO.find_one_or_none(telegram_id=message.from_user.id)
    #
    # if not user:
    #     await UserDAO.add(
    #         telegram_id=message.from_user.id,
    #         first_name=message.from_user.first_name,
    #         username=message.from_user.username
    #     )
    #
    # await greet_user(message, is_new_user=not user)
    user = await UserDAO.find_one_or_none(telegram_id=message.from_user.id)

    if not user:
        await state.set_state(Form.waiting_for_phone)
        await message.answer('Привет!\n\nПожалуйста, поделись своим номером телефона '
                             'для завершения регистрации', reply_markup=register_keyboard())
    else:
        await greet_user(message, is_new_user=not user, phone_number=user.phone_number)


@user_router.message(F.contact)
async def process_contact(message:Message, state:FSMContext):
    user = await UserDAO.find_one_or_none(telegram_id=message.from_user.id)

    if not user:
        await UserDAO.add(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            username=message.from_user.username,
            phone_number=message.contact.phone_number  # Сохраняем номер телефона в БД
        )

    await greet_user(message, is_new_user=True, phone_number=user.phone_number)
    await state.set_state(None)


@user_router.message(F.text == '🔙 Назад')
async def cmd_back_home(message: Message) -> None:
    await greet_user(message, is_new_user=False)


@user_router.message(F.text == "ℹ️ О нас")
async def about_us(message: Message):
    kb = app_keyboard(user_id=message.from_user.id, first_name=message.from_user.first_name)
    await message.answer(get_about_us_text(), reply_markup=kb)


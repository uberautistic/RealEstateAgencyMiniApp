import logging
import requests
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.api.schemas import ApplicationData
from app.bot.create_bot import bot
from app.api.dao import ApplicationDAO, UserDAO, CityDAO
from app.bot.keyboards.kbs import main_keyboard
from app.config import settings

router = APIRouter(prefix='/api', tags=['API'])
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@router.post("/application", response_class=JSONResponse)
async def create_appointment(request: Request):
    # получение данных и валидация
    data = await request.json()
    validated_data = ApplicationData(**data)
    city_id, city_name = validated_data.city.split('_')
    application_type, application_type_name = validated_data.application_type.split('/')

    # сообщение клиенту
    message = (
        f"🎉 <b>{validated_data.name}, ваша заявка успешно принята!</b>\n\n"
        "💬 <b>Информация о вашей заявке:</b>\n"
        f"🏙<b>Город:</b> {city_name}\n"
        f"✉️<b>Тип заявки:</b> {application_type_name}\n"
        f"📄<b>Заявка:</b> {validated_data.application_text}\n"
        "Спасибо за выбор нашего агентства! ✨ В скором времени с вами свяжется наш сотрудник."
    )

    # сообщение админу
    admin_message = (
        "🔔 <b>Новая заявка!</b>\n\n"
        "📕 <b>Детали заявки:</b>\n"
        f"👤 <b>Имя клиента:</b> {validated_data.name}\n"
        f"📞<b>Номер телефона:</b> {validated_data.contact}\n"
        f"🏙<b>Город:</b> {city_name}\n"
        f"✉️<b>Тип заявки:</b> {application_type_name}\n"
        f"📄<b>Заявка:</b> {validated_data.application_text}\n"
    )

    # запись заявки в БД
    await ApplicationDAO.add(
        user_id=validated_data.user_id,
        city_id=city_id,
        client_name=validated_data.name,
        contact=validated_data.contact,
        application_text=validated_data.application_text,
        application_type=application_type
    )
    user = await UserDAO.find_one_or_none(telegram_id=validated_data.user_id)
    admin = await UserDAO.find_one_or_none(telegram_id=settings.ADMIN_ID)
    kb = main_keyboard(user_id=validated_data.user_id, first_name=validated_data.name, phone_number=user.phone_number)
    adminkb = main_keyboard(user_id=admin.telegram_id, first_name=admin.first_name, phone_number=admin.phone_number)
    # отправка сообщений клиенту, админу и боту для уведомлений
    await bot.send_message(chat_id=validated_data.user_id, text=message, reply_markup=kb)
    await bot.send_message(chat_id=settings.ADMIN_ID, text=admin_message, reply_markup=adminkb)
    try:
        url =f'{settings.INFOBASE_SITE}/telegram/applications/'
        headers = {'Content-Type': 'application/json'}
        data = {
            'telegram_id': user.telegram_id,
            'city_name': city_name,
            'phone_number': validated_data.contact,
            'application_text':validated_data.application_text,
            'application_type':application_type
        }
        response = requests.post(url=url, headers=headers, json=data)
        logging.info(f'Код состояния: {response.status_code}, Ответ: {response.json()["response"]}')
    except Exception as e:
        logging.error(f'Ошибка: {e}')

    return {"message": "success!"}

@router.get("/phone_number", response_class=JSONResponse)
async def get_phone_number(request: Request, user_id:int=None):
    # метод для заполнения формы при переходе с начальной странички на страничку формы
    user = await UserDAO.find_one_or_none(telegram_id=user_id)
    phone_number = user.phone_number if user else "no user"

    return {"phone_number": phone_number}

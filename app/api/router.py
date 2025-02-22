from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.api.schemas import ApplicationData
from app.bot.create_bot import bot
from app.api.dao import ApplicationDAO
from app.bot.keyboards.kbs import main_keyboard
from app.config import settings

router = APIRouter(prefix='/api', tags=['API'])


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
    kb = main_keyboard(user_id=validated_data.user_id, first_name=validated_data.name)
    # отправка сообщений клиенту, админу и боту для уведомлений
    await bot.send_message(chat_id=validated_data.user_id, text=message, reply_markup=kb)
    await bot.send_message(chat_id=settings.ADMIN_ID, text=admin_message, reply_markup=kb)

    return {"message": "success!"}

from pydantic import BaseModel, Field
from datetime import date, time

class ApplicationData(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Имя клиента")
    contact: str = Field(..., min_length=2, max_length=50, description="Номер телефона")
    city: str = Field(..., min_length=2, max_length=50, description="Город")
    application_type: str = Field(..., min_length=2, max_length=50, description="Тип заявки")
    application_text: str = Field(..., min_length=2, max_length=200, description="Текст заявки")

    user_id: int = Field(..., description="ID пользователя Telegram")
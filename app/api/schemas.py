from pydantic import BaseModel, Field


class ApplicationData(BaseModel):
    name: str = Field(description="Имя клиента")
    contact: str = Field(description="Номер телефона")
    city_id: str = Field(description="Код города в информационной базе", default=None)
    application_type: str = Field(description="Тип заявки", default=None)
    application_text: str = Field(description="Текст заявки")
    object_id: str = Field(description="Код объекта в информационной базе", default='0')

    user_id: int = Field(description="ID пользователя Telegram")

class RealEstateObject(BaseModel):
    id: str = Field(description="Код объекта в Информационной базе")
    name: str = Field(description="Краткое название объекта")
    city: str = Field(description="Город")
    district: str = Field(description="Район")
    price: str = Field(description="Цена")
    status: str = Field(description="Статус")
    image: str = Field(description="URL изображения")

class City(BaseModel):
    id: str = Field(description="Код города в информационной базе")
    name: str = Field(description="Название города")

class RealEstateType(BaseModel):
    id: str = Field(description="Код типа недвижимости в информационной базе")
    name: str = Field(description="Название")

class RealEstateObjectFull(BaseModel):
    id: str = Field(description="Код объекта в Информационной системе")
    name: str = Field(description="Краткое название объекта")
    district: str = Field(description="Район")
    address: str = Field(description="Адрес")
    longitude: float = Field(description="Долгота")
    latitude: float = Field(description="Широта")
    description: str =Field(description="Описание")
    price: str = Field(description="Цена")
    status: str = Field(description="Статус")
    communal_services: str = Field(description="Коммунальные услуги")
    commission_percent: int = Field(description="Комиссия в процентах")
    commission: str = Field(description="Комиссия")
    images: list[str] = Field(description="URL изображений")

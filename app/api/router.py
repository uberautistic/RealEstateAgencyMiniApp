import logging
import requests
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.api.schemas import ApplicationData
from app.config import settings

router = APIRouter(prefix='/api', tags=['API'])
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@router.post("/application", response_class=JSONResponse)
async def create_application(request: Request):
    data = await request.json()
    application_data= ApplicationData(**data)
    try:
        url=f'{settings.INFOBASE_SITE}/telegram/applications/'
        headers={'Content-Type': 'application/json'}
        data ={
            'telegram_id':application_data.user_id,
            'city_id':application_data.city_id,
            'phone_number':application_data.contact,
            'application_type':application_data.application_type,
            'application_text':application_data.application_text,
            'object_id':application_data.object_id
        }
        response = requests.post(url=url,headers=headers,json=data)
        logging.info(f'Код состояния: {response.status_code}, Ответ: {response.json()}')
        result = "success" if response.status_code == 200 else "error"
    except Exception as e:
        logging.error(f'Ошибка: {e}')
        result = e

    return {"message":result}
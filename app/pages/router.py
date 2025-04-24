from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.testing.plugin.plugin_base import logging
from app.api.dao import UserDAO
from app.api.schemas import RealEstateObject, City,RealEstateType, RealEstateObjectFull
from app.config import settings
import requests
import logging

router = APIRouter(prefix='', tags=['Фронтенд'])
templates = Jinja2Templates(directory='app/templates')


@router.get("/home", response_class=HTMLResponse)
async def read_root(
        request: Request,
        user_id: int = None):
    context = {
        "request": request,
        "user_id": user_id
    }
    user = await UserDAO.find_one_or_none(telegram_id=user_id)
    if user:
        context['name']=user.first_name
        context['phone_number']=user.phone_number
    try:
        response = requests.get(f"{settings.INFOBASE_SITE}/telegram/objects/")
        logging.info(f"Код: {response.status_code}")
        data = response.json()
        objects = [RealEstateObject(**item) for item in data['objects']]
        cities = [City(**item) for item in data['cities']]
        types = [RealEstateType(**item) for item in data['types']]
        context["objects"]=objects
        context["cities"]=cities
        context["types"]=types
    except Exception as e:
        logging.error(f"Ошибка: {e}")

    return templates.TemplateResponse("home.html", context)

@router.get("/filter", response_class=HTMLResponse)
async def read_root(
        request: Request,
        filter_city: str = None,
        filter_property_type: str = None,
        filter_deal_type: str = None,
        price_from: int = None,
        price_to: int = None,
        area_from: int = None,
        area_to: int = None,
        user_id: str = None):

    params ={}

    if filter_city:
        params['city'] = filter_city

    if filter_property_type:
        params['type'] = filter_property_type

    if filter_deal_type:
        params['status'] = filter_deal_type

    if price_from:
        params['price_from'] = price_from

    if price_to:
        params['price_to'] = price_to

    if area_from:
        params['area_from'] = area_from

    if area_to:
        params['area_to'] = area_to

    context = {
        'request': request,
        'user_id': user_id,
    }

    user = await UserDAO.find_one_or_none(telegram_id=user_id)

    if user:
        context['name'] = user.first_name
        context['phone_number'] = user.phone_number
    try:
        url = f'{settings.INFOBASE_SITE}/telegram/objects/'
        response = requests.get(url=url, params=params)
        logging.info(f"Код: {response.status_code}")
        data = response.json()
        objects = [RealEstateObject(**item) for item in data['objects']]
        context['objects']=objects
    except Exception as e:
        logging.error(f'Ошибка: {e}')

    return templates.TemplateResponse("objects.html", context)

@router.get("/object/{object_id}",response_class=HTMLResponse)
async def read_root(
        request: Request,
        object_id: str= None,
        user_id: int = None):
    context = {
        'request':request,
        'user_id':user_id,
        'yandex_map_api_key': settings.YANDEX_MAPS_API_KEY
    }

    user = await UserDAO.find_one_or_none(telegram_id=user_id)

    if user:
        context['name'] = user.first_name
        context['phone_number'] = user.phone_number

    if object_id:
        url = f'{settings.INFOBASE_SITE}/telegram/objects'
        params = {'id':object_id}
        try:
            response = requests.get(url=url,params=params)
            logging.info(f"Код: {response.status_code}")
            data = response.json()
            object_data = RealEstateObjectFull(**data)
            context['object']=object_data
        except Exception as e:
            logging.error(f'Ошибка: {e}')
            context['message']='При отправке запроса произошла ошибка'
    else:
        context['message']='Не указан айди объекта'

    return templates.TemplateResponse('property.html', context)


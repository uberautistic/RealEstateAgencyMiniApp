from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from app.api.dao import CityDAO, ApplicationDAO, UserDAO
from app.config import settings

router = APIRouter(prefix='', tags=['Фронтенд'])
templates = Jinja2Templates(directory='app/templates')


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"request": request}

    return templates.TemplateResponse("index.html", context)


@router.get("/form", response_class=HTMLResponse)
async def read_root(request: Request, user_id: int = None, first_name: str = None, phone_number: str = None):
    cities = await CityDAO.find_all()
    context = {
        "request": request,
        "name": first_name,
        "phone_number": phone_number,
        "cities": cities,
        "user_id": user_id
    }

    return templates.TemplateResponse("form.html", context)

@router.get("/admin", response_class=HTMLResponse)
async def read_root(request: Request, admin_id:int=None):
    context = {
        "request":request,
        "access":False,
        "is_admin":True,
        "title_h1":"Админ панель"
    }
    if admin_id is None or admin_id!=settings.ADMIN_ID:
        context["message"]="У вас нет прав для просмотра информации о заявках"
    else:
        context["access"]=True
        applications = await ApplicationDAO.get_all_applications()
        if len(applications):
            context["applications"]= applications
        else:
            context["message"]= "Нет заявок 😔"

    return templates.TemplateResponse("applications.html", context)

@router.get("/applications", response_class=HTMLResponse)
async def read_root(request: Request, user_id: int = None):
    context = {
        "request": request,
        "access": False,
        "is_admin": False,
        "title_h1": "Мои заявки"
    }
    user_check = await UserDAO.find_one_or_none(telegram_id=user_id)

    if user_id is None or user_check is None:
        context["message"] = "Пользователь, по которому нужно отобразить заявки, не указан или не найден в базе данных"
    else:
        applications = await ApplicationDAO.get_applications_by_user(user_id=user_id)
        context["access"] = True
        if len(applications):
            context["applications"] = applications
        else:
            context["message"] = "У вас нет заявок 😔"

    return templates.TemplateResponse("applications.html", context)

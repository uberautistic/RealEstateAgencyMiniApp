from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from app.api.dao import CityDAO

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

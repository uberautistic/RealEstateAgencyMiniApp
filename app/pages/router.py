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
async def read_root(request: Request, user_id: int = None, first_name: str = None):
    cities = await CityDAO.find_all()
    context = {
        "request": request,
        "user_id": user_id,
        "name": first_name,
        "cities": cities
    }

    return templates.TemplateResponse("form.html", context)

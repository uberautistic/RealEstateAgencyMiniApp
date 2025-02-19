from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from app.dao.base import BaseDAO
from app.api.models import User, City, Application
from app.db import async_session_maker

class UserDAO(BaseDAO):
    model = User

class CityDAO(BaseDAO):
    model = City

class ApplicationDAO(BaseDAO):
    model = Application

    @classmethod
    async def get_applications_by_user(cls, user_id: int):
        async with async_session_maker() as session:
            try:
                query = (
                    select(cls.model)
                    .options(joinedload(cls.model.city))
                    .filter_by(user_id=user_id)
                )
                result = await session.execute(query)
                applications = result.scalars().all()
                return [
                    {
                        "application_id": app.id,
                        "user_id": app.user_id,
                        "city_name": app.city.name,
                        "client_name": app.client_name,
                        "contact":app.contact,
                        "application_text": app.application_text
                    }
                    for app in applications
                ]
            except SQLAlchemyError as e:
                print(f"Error while fetching applications for user {user_id}: {e}")
                return None

    @classmethod
    async def get_all_applications(cls):

        async with async_session_maker() as session:
            try:
                query = (
                    select(cls.model)
                    .options(joinedload(cls.model.city))
                )
                result = await session.execute(query)
                applications = result.scalars().all()

                return [
                    {
                        "application_id": app.id,
                        "user_id": app.user_id,
                        "city_name": app.city.name,
                        "client_name": app.client_name,
                        "contact":app.contact,
                        "application_text": app.application_text
                    }
                    for app in applications
                ]
            except SQLAlchemyError as e:
                print(f"Error while fetching all applications: {e}")
                return None
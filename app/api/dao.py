from app.dao.base import BaseDAO
from app.api.models import User

class UserDAO(BaseDAO):
    model = User
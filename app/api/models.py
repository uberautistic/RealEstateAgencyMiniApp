import enum

from sqlalchemy import String, BigInteger, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger,
                                             primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=True)

    applications: Mapped[list["Application"]] = relationship(back_populates="user")


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    applications: Mapped[list["Application"]] = relationship(back_populates="city")


class Application(Base):
    __tablename__ = 'applications'

    class ApplicationTypeEnum(enum.Enum):
        sell = "Продать"
        rent_out = "Сдать"
        buy = "Приобрести"
        rent = "Снять"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.telegram_id'))
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.id'))
    client_name: Mapped[str] = mapped_column(String, nullable=False)
    contact: Mapped[str] = mapped_column(String, nullable=False)
    application_text: Mapped[str] = mapped_column(String, nullable=False)
    application_type: Mapped[ApplicationTypeEnum] = mapped_column(Enum(ApplicationTypeEnum), nullable=False)

    user: Mapped["User"] = relationship(back_populates="applications")
    city: Mapped["City"] = relationship(back_populates="applications")

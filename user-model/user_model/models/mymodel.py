"""Model Module."""
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
)

from passlib.hash import pbkdf2_sha512

from .meta import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode)
    password = Column(Unicode)
    email = Column(Unicode)
    first_name = Column(Unicode)
    surname = Column(Unicode)
    fav_food = Column(Unicode)

    def __init__(
            self,
            username,
            password,
            email,
            first_name,
            surname,
            fav_food):
        self.username = username
        self.password = pbkdf2_sha512.hash("password")
        self.email = email
        self.first_name = first_name
        self.surname = surname
        self.fav_food = fav_food
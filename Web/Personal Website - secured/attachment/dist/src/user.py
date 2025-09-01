from __future__ import annotations
import dataclasses
import shelve
from werkzeug.security import generate_password_hash, check_password_hash

@dataclasses.dataclass
class Config:
    mode: str = 'light'

@dataclasses.dataclass
class User:
    username: str
    password: str
    config: Config

    @staticmethod
    def _merge_info(src, user: User, *, depth=0):
        if depth > 3:
            raise Exception("Reached maximum depth")
        for k, v in src.items():
            if hasattr(user, "__getitem__"):
                if user.get(k) and isinstance(v, dict):
                    User._merge_info(v, user.get(k), depth=depth+1)
                else:
                    user[k] = v
            elif hasattr(user, k) and isinstance(v, dict):
                User._merge_info(v, getattr(user, k), depth=depth+1)
            else:
                setattr(user, k, v)

    @staticmethod
    def merge_info(src, user: User):
        User._merge_info(src, user)
        with shelve.open('users.db', writeback=True) as db:
            db[user.username] = user
            db.sync()

    @staticmethod
    def create(username: str, password: str) -> User:
        with shelve.open('users.db', writeback=True) as db:
            if username in db:
                raise Exception("The user already exists")
            user = User(username, generate_password_hash(password), Config())
            db[username] = user
            db.sync()
            return user

    @staticmethod
    def verify(username: str, password: str) -> None:
        with shelve.open('users.db') as db:
            if username not in db:
                raise Exception("The user doesn't exist")
            user: User = db[username]
            if not check_password_hash(user.password, password):
                raise Exception("Wrong password")

    @staticmethod
    def get(username: str) -> User:
        with shelve.open('users.db', writeback=True) as db:
            if username not in db:
                raise Exception("The user doesn't exist")
            return db[username]
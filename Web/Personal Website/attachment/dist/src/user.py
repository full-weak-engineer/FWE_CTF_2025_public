from __future__ import annotations
import dataclasses
from werkzeug.security import generate_password_hash, check_password_hash

users: dict[str,User] = {}


# TODO: Increase more options
@dataclasses.dataclass
class Config:
    mode: str = 'light'

@dataclasses.dataclass
class User:
    username: str
    password: str
    config: Config
    
    @staticmethod
    def merge_info(src, user, *, depth=0):
        if depth > 3:
            raise Exception("Reached maximum depth")
        for k, v in src.items():
            if hasattr(user, "__getitem__"):
                if user.get(k) and type(v) == dict:
                    User.merge_info(v, user.get(k),depth=depth+1)
                else:
                    user[k] = v
            elif hasattr(user, k) and type(v) == dict:
                User.merge_info(v, getattr(user, k),depth=depth+1)
            else:
                setattr(user, k, v)
                
    @staticmethod
    def create(username: str, password: str):
        if username in users:
            raise Exception("The user already exist")
        user = User(username, generate_password_hash(password), Config())
        users[username] = user
        return user

    @staticmethod
    def verify(username: str, password: str):
        if username not in users:
            raise Exception("The user doesn't exist")
        user = users[username]
        if not check_password_hash(user.password, password):
            raise Exception("Wrong password")
        return
    
    @staticmethod
    def get(username: str):
        if username not in users:
            raise Exception("The user doesn't exist")
        return users[username]
            
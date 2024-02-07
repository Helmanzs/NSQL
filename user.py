from werkzeug.security import generate_password_hash, check_password_hash
import typing

class User:
    def __init__(self, username: str, password: str, email: str) -> typing.Type['User']:
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    @staticmethod
    def check_password(password_hash, password: str) -> bool:
        return check_password_hash(password_hash, password)
    
    @staticmethod
    def to_json(user):
        return {
            'username': user.username,
            'password': user.password,
            'email': user.email
        }
    
    @staticmethod
    def from_json(user_json: str) -> typing.Type['User']:
        user = User(user_json['username'], "", user_json['email'])
        user.password_hash = user_json['password']
        return user
    
    
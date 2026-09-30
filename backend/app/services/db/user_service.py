from backend.app.gateways.db.user_gateways import UsersGateway
from backend.app.factories.user_factory import UserFactory
from backend.app.validators.user_validators import UserValidator

user_gateway= UsersGateway()
user_factory=UserFactory()
user_validator=UserValidator()

def create_user(username, password):
    user_validator.validate_username_available(username)
    user_validator.validate_username(username)
    user_validator.validate_password(password)
    user_dict=user_factory.create_user(username=username, password=password)
    return user_dict

def get_user_by_id(user_id):
    return user_gateway.get_user_by_id(user_id)

def get_all_users():
    return user_gateway.get_all_users()

def get_user_by_username(username):
    return user_gateway.get_user_by_username(username)
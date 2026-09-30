from dataclasses import dataclass
from backend.app.gateways.db.user_gateways import UsersGateway
from backend.app.models.db.user import User

@dataclass
class UserValidator:

    def __init__(self) -> None:
            self.user_gateway=UsersGateway()

    def not_exist(self,user: User):
        if user is None:
            raise Exception("user não existe")
        return user

    def validate_username_available(self,username: str):
        user = self.user_gateway.get_user_by_username(username)
        if user is not None:
            raise ValueError(f'O username "{username}" já está sendo utilizado.')
    
    def validate_username(self,username: str) -> None:
        if not username:
            raise ValueError("Username é obrigatório")

        if len(username) < 3:
            raise ValueError("Username deve ter pelo menos 3 caracteres")

        if len(username) > 30:
            raise ValueError("Username deve ter no máximo 30 caracteres")

        if not username.isalnum():
            raise ValueError(
                "Username deve conter apenas letras e números"
            )


    def validate_password(self,password: str) -> None:
        if len(password) < 8:
            raise ValueError(
                "Senha deve ter pelo menos 8 caracteres"
            )

        if not any(c.isupper() for c in password):
            raise ValueError(
                "Senha deve possuir uma letra maiúscula"
            )

        if not any(c.islower() for c in password):
            raise ValueError(
                "Senha deve possuir uma letra minúscula"
            )

        if not any(c.isdigit() for c in password):
            raise ValueError(
                "Senha deve possuir um número"
            )
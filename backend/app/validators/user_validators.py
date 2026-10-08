from dataclasses import dataclass

from backend.app.gateways.db.user_gateways import UsersGateway
from backend.app.models.db.user import User
from backend.app.utils.ids import verify_password

from backend.app.utils.user_exceptions import (
    UserNotFoundError,
    UsernameAlreadyExistsError,
    InvalidUsernameError,
    InvalidPasswordError,
    InvalidLoginError,
)


@dataclass
class UserValidator:

    def __init__(self) -> None:
        self.user_gateway = UsersGateway()


    def not_exist(self, user: User):
        if user is None:
            raise UserNotFoundError(
                "Usuário não existe"
            )

        return user


    def validate_username_available(
        self,
        username: str
    ):
        user = (
            self.user_gateway
            .get_user_by_username(username)
        )

        if user is not None:
            raise UsernameAlreadyExistsError(
                f'O username "{username}" já está sendo utilizado.'
            )


    def validate_username(
        self,
        username: str
    ) -> None:

        if not username:
            raise InvalidUsernameError(
                "Username é obrigatório"
            )

        if len(username) < 3:
            raise InvalidUsernameError(
                "Username deve ter pelo menos 3 caracteres"
            )

        if len(username) > 30:
            raise InvalidUsernameError(
                "Username deve ter no máximo 30 caracteres"
            )

        if not username.isalnum():
            raise InvalidUsernameError(
                "Username deve conter apenas letras e números"
            )


    def validate_password(
        self,
        password: str
    ) -> None:

        if not password:
            raise InvalidPasswordError(
                "Senha é obrigatória"
            )

        if len(password) < 8:
            raise InvalidPasswordError(
                "Senha deve ter pelo menos 8 caracteres"
            )

        if not any(
            c.isupper()
            for c in password
        ):
            raise InvalidPasswordError(
                "Senha deve possuir uma letra maiúscula"
            )

        if not any(
            c.islower()
            for c in password
        ):
            raise InvalidPasswordError(
                "Senha deve possuir uma letra minúscula"
            )

        if not any(
            c.isdigit()
            for c in password
        ):
            raise InvalidPasswordError(
                "Senha deve possuir um número"
            )


    def validate_login(
        self,
        user: User,
        password: str
    ) -> User:

        if user is None:
            raise InvalidLoginError(
                "Username ou senha inválidos"
            )

        if not verify_password(
            password,
            user.password_hash
        ):
            raise InvalidLoginError(
                "Username ou senha inválidos"
            )

        return user
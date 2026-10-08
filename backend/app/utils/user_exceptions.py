class UserNotFoundError(Exception):
    pass


class UsernameAlreadyExistsError(Exception):
    pass


class InvalidUsernameError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class InvalidLoginError(Exception):
    pass
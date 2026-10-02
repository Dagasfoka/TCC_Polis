import random
import string
import uuid
import secrets
import hashlib


def generate_room_code(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_player_id():
    return str(uuid.uuid4())


def generate_player_token():
    return secrets.token_urlsafe(32)


def generate_password_hash(password: str) -> str:
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def verify_password(
    password: str,
    password_hash: str
) -> bool:

    generated_hash = generate_password_hash(
        password
    )

    return generated_hash == password_hash  
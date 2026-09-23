# Gerar UUID, códigos de sala, tokens auxiliares.
import random
import string
import uuid
import secrets

def generate_room_code(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def generate_player_id():
    return str(uuid.uuid4())

def generate_player_token():
    return secrets.token_urlsafe(32)
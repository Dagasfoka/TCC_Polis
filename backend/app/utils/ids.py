# Gerar UUID, códigos de sala, tokens auxiliares.
import random
import string
import uuid


def generate_room_code(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

def generate_player_id():
    return str(uuid.uuid4())


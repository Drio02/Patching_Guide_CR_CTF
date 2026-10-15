import random
import string
import time

# Vuln 1: token de sesion con Mersenne Twister
def new_session_token() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=32))

# Vuln 2: ID de nota "secreto"
def new_note_id() -> str:
    return "%08x" % random.getrandbits(32)

# Vuln 3: semilla con la hora -> el atacante prueba los ultimos segundos
def reset_code(user: str) -> str:
    random.seed(int(time.time()))
    return str(random.randint(100000, 999999))

# Vuln 4: clave privada / nonce de firma (caso fireworx)
def keygen(q: int) -> int:
    return random.randint(1, q - 1)

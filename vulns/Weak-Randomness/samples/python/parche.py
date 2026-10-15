import secrets
import string

ALPHABET = string.ascii_letters + string.digits

# Patch 1: mismo alfabeto y longitud (el checker no nota el cambio), pero con CSPRNG
def new_session_token() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(32))

# Patch 2: mismo formato de 8 hex
def new_note_id() -> str:
    return secrets.token_hex(4)

# Patch 3: sin semilla; secrets no se puede sembrar
def reset_code(user: str) -> str:
    return str(100000 + secrets.randbelow(900000))

# Patch 4: clave en [1, q-1]
def keygen(q: int) -> int:
    return secrets.randbelow(q - 1) + 1

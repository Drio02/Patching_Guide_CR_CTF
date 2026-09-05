# Vuln 1
# AES en modo ECB
# No hay IC ni auth
# Filtra estructura 2 bloques identicos -> Permite chosen-plaintext / ECB byte-at-a-time

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

KEY = b"0123456789abcdef"

def encrypt_note(plaintext: bytes) -> bytes:
    cipher = AES.new(KEY, AES.MODE_ECB)          # ECB: mismo bloque → mismo ciphertext
    return cipher.encrypt(pad(plaintext, 16))

# Vuln 2
# IV constante
# Mensjae con mismo prefijo mismo cipher -> fuga de info

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

KEY = b"my16bytekey12345"
IV  = b"0000000000000000"   # IV fijo y predecible

def enc(data: bytes) -> bytes:
    cipher = AES.new(KEY, AES.MODE_CBC, IV)   # mismo IV siempre
    return cipher.encrypt(pad(data, 16))

# Vuln 3
# Reutilizacion de Nonce
# CTR/GCM con nonce fijo -> dos mensajes cifrados con el mismo keystream

from Crypto.Cipher import AES
from Crypto.Util import Counter

KEY   = b"key-of-16-bytes!"
NONCE = 0x00                                  # nonce/contador inicial fijo

def enc(msg: bytes) -> bytes:
    ctr = Counter.new(128, initial_value=NONCE)
    return AES.new(KEY, AES.MODE_CTR, counter=ctr).encrypt(msg)
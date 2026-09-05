# Pathc 1
# AES-GCM, auth

import os
from Crypto.Cipher import AES

KEY = bytes.fromhex(os.environ["ENC_KEY"])

def encrypt_note(plaintext: bytes) -> bytes:
    nonce = os.urandom(12)                    # nonce único por mensaje
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(plaintext)
    return nonce + tag + ct                   # se guarda todo junto

# Patch 2

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

KEY = bytes.fromhex(os.environ["ENC_KEY"])

def enc(data: bytes) -> bytes:
    iv = os.urandom(16)                        # IV aleatorio por mensaje
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(data, 16))

# Patch 3

import os
from Crypto.Cipher import AES

KEY = bytes.fromhex(os.environ["ENC_KEY"])

def enc(msg: bytes) -> bytes:
    nonce = os.urandom(12)                     # nonce único por mensaje
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(msg)
    return nonce + tag + ct
# Parche: Crypto

## Estrategia

1. **Rotar las claves hardcodeadas** a un valor aleatorio propio, persistido en un archivo/volumen (para que sobreviva reinicios y lo compartan todos los workers).
2. **Cifrado autenticado**: AES-GCM o ChaCha20-Poly1305 con nonce aleatorio por mensaje.
3. **MAC con HMAC**, nunca `hash(key + msg)`.
4. **Comparación en tiempo constante** para todo secreto (tokens, firmas, MACs, hashes de password).
5. **CSPRNG** para claves, nonces y tokens.
6. **Firmas**: nonce aleatorio (o RFC 6979), verificación de rangos, errores genéricos.

| Necesidad | Python | Node | Go | Java | PHP | C (OpenSSL) |
|---|---|---|---|---|---|---|
| Cifrado autenticado | `AESGCM` (`cryptography`) / `AES.MODE_GCM` | `createCipheriv('aes-256-gcm')` | `cipher.NewGCM` | `Cipher.getInstance("AES/GCM/NoPadding")` | `openssl_encrypt(..., 'aes-256-gcm', ..., $tag)` | `EVP_aes_256_gcm()` |
| HMAC | `hmac.new(k, m, sha256)` | `createHmac('sha256', k)` | `hmac.New(sha256.New, k)` | `Mac.getInstance("HmacSHA256")` | `hash_hmac('sha256', $m, $k)` | `HMAC(EVP_sha256(), ...)` |
| Comparar | `hmac.compare_digest` | `crypto.timingSafeEqual` | `subtle.ConstantTimeCompare` | `MessageDigest.isEqual` | `hash_equals` | `CRYPTO_memcmp` |
| Random | `secrets` | `crypto.randomBytes` | `crypto/rand` | `SecureRandom` | `random_bytes` | `RAND_bytes` / `getrandom` |
| Passwords | `bcrypt` / `argon2-cffi` | `bcrypt` | `x/crypto/bcrypt` | `BCryptPasswordEncoder` | `password_hash` | `crypt()` con `$6$`/`$2b$` |

## Firmas DSA/ECDSA caseras

```python
# Firma: k aleatorio por firma (o RFC 6979: k = HMAC_DRBG(x, H(m)))
k = secrets.randbelow(q - 1) + 1

# Verificacion: rechazar r, s fuera de rango ANTES de invertir s
if not (0 < r < q and 0 < s < q):
    return False

# Error generico: nunca devolver la firma/MAC esperada
return web.Response(status=400, text="bad signature")
```

## Errores comunes

- **Cambiar el formato de lo ya guardado**: si los flags están cifrados con la clave vieja, rotarla rompe el `getflag` del checker para los flags anteriores. Opciones: descifrar con la vieja y cifrar con la nueva al leer, o rotar en el borde de una ronda.
- Generar la clave con `os.urandom` al arrancar sin persistirla: cada worker/reinicio tiene una clave distinta → sesiones inválidas → SLA caído.
- Migrar passwords a bcrypt sin migrar los existentes: los usuarios del checker ya no pueden loguear.
- Parchear el ECB pero dejar la clave hardcodeada (o al revés).
- MD5 en un proof-of-work, cache key o checksum de integridad no adversarial **no es una vulnerabilidad**. No perder tiempo ahí.

## Defensa en profundidad

- Preferir librerías de alto nivel (`cryptography.fernet`, libsodium `secretbox`, `nacl`) sobre primitivas sueltas.
- Revisar todo el archivo de crypto después del primer parche: suele haber 3 o 4 bugs.

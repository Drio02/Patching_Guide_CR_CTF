# Crypto

## Qué es

Uso incorrecto de primitivas criptográficas: la primitiva es segura, pero la forma de usarla no. Los servicios de A/D suelen traer criptografía "casera" con varios bugs independientes en el mismo archivo.

| Bug | Consecuencia |
|---|---|
| Clave hardcodeada | Todos los equipos tienen el código → descifran/firman lo que quieran |
| AES-ECB | Bloques iguales → ciphertext igual; ataques byte-at-a-time y cut-and-paste (`role=admin`) |
| IV/nonce fijo o reutilizado (CBC, CTR, GCM) | Keystream repetido → XOR de dos mensajes; en GCM permite forjar tags |
| CBC sin MAC | Padding oracle, bit flipping |
| `MAC = H(key ‖ msg)` | Length extension (MD5/SHA1/SHA256) |
| Comparación de secretos con `==`/`memcmp` | Timing attack |
| PRNG no criptográfico (`random`, `Math.random`, `rand`) | Tokens/claves predecibles |
| DSA/ECDSA con nonce `k` fijo o derivado sin el mensaje | Dos firmas → `k` → clave privada |
| Verificación DSA/ECDSA sin chequear `0 < r, s < q` | `r=1, s=0` verifica cualquier mensaje |
| Oráculo de firma (el error devuelve la firma esperada) | Login replicando el valor |
| RSA sin padding, `e` pequeño, primos pequeños/compartidos | Descifrado / factorización |
| JWT con `alg: none`, secreto débil, confusión RS256/HS256 | Forjar tokens |

## Cómo identificarla en código

```bash
rg -n -i 'MODE_ECB|aes-\d+-ecb|AES_encrypt\(|iv\s*=\s*b?"|nonce\s*=\s*\d|Counter\.new'
rg -n -i 'md5|sha1|hashlib\.\w+\(.*key'
rg -n '==\s*(sig|signature|mac|hmac|token|hash)|memcmp\(|strcmp\(.*(token|hash|sig)' -i
rg -n 'random\.|Math\.random|\brand\(|srand\(|math/rand'
rg -n 'k\s*=\s*H\(|inverse\(s'
```

## Impacto en A/D

- **auth-bypass**: forjar cookies/tokens/firmas para entrar como el usuario que tiene el flag.
- **flag-leak**: descifrar los flags que el servicio guarda cifrados.

## Referencias

- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [Cryptopals](https://cryptopals.com/) (practicar los ataques)
- [CWE-327](https://cwe.mitre.org/data/definitions/327.html), [CWE-323](https://cwe.mitre.org/data/definitions/323.html), [CWE-347](https://cwe.mitre.org/data/definitions/347.html)

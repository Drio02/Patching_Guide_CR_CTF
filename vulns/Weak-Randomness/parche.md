# Parche: Aleatoriedad débil

## Estrategia

Reemplazar el PRNG por el CSPRNG del lenguaje **solo en los valores de seguridad**:

| Lenguaje | Inseguro | Seguro |
|---|---|---|
| Python | `random.*` | `secrets.token_hex(16)`, `secrets.token_urlsafe(16)`, `secrets.randbelow(n)`, `secrets.choice(seq)` |
| Node | `Math.random()` | `crypto.randomBytes(16)`, `crypto.randomUUID()`, `crypto.randomInt(n)` |
| Browser | `Math.random()` | `crypto.getRandomValues(new Uint8Array(16))` |
| PHP | `rand`, `mt_rand`, `uniqid` | `random_bytes(16)`, `random_int(a, b)` |
| Java | `Random`, `Math.random` | `SecureRandom` |
| Go | `math/rand` | `crypto/rand` (`rand.Read`, `rand.Int`, `rand.Text()` en 1.24+) |
| C# | `System.Random` | `RandomNumberGenerator.GetBytes(16)` |
| Ruby | `rand` | `SecureRandom.hex(16)` |
| C | `rand`, `srand(time(NULL))` | `getrandom(buf, n, 0)` o leer `/dev/urandom` |

## Errores comunes

- **Cambiar un PRNG cuya salida debe ser reproducible**: si el servicio hace `srand(seed)` para regenerar un keystream que descifra datos guardados, cambiarlo rompe la lectura de flags viejos. En ese caso, arreglar la parte explotable (semilla predecible, overflow) y mantener la derivación determinista.
- Cambiar el **formato** del token (largo, alfabeto) cuando el checker lo valida con una regex. Mantener el mismo alfabeto y longitud: `''.join(secrets.choice(ALPHABET) for _ in range(N))`.
- "Mejorar" la semilla con `time() ^ getpid()`: sigue siendo predecible.
- `random.SystemRandom()` en Python es seguro; no hace falta reemplazarlo.
- Perder tiempo en `Math.random()` del frontend para efectos visuales: falso positivo.

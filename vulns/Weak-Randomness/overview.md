# Aleatoriedad débil (Weak Randomness)

## Qué es

Se usa un generador pseudoaleatorio **no criptográfico** para valores que deben ser impredecibles: tokens de sesión, IDs de notas, códigos de reset, passwords generados, nombres de archivo, claves, nonces.

| Generador | Por qué es predecible |
|---|---|
| Python `random` (Mersenne Twister) | 624 salidas de 32 bits recuperan el estado completo (`randcrack`) |
| JS `Math.random()` (V8 xorshift128+) | Unas pocas salidas recuperan el estado (z3) |
| C `rand()` + `srand(time(NULL))` | La semilla es la hora en segundos: se prueban los últimos N segundos |
| PHP `rand()` / `mt_rand()` / `uniqid()` | MT19937 recuperable; `uniqid` es la hora en microsegundos |
| Java `java.util.Random` | LCG de 48 bits: dos salidas recuperan el estado |
| Go `math/rand` | Determinista; en Go < 1.20 la semilla por defecto era 1 |

## Cómo identificarla en código

```bash
rg -n 'random\.(randint|choice|choices|random|randbytes|getrandbits|shuffle)|numpy\.random'
rg -n 'Math\.random|mt_rand|\brand\(|srand\(|uniqid\(|math/rand|new Random\(|java\.util\.Random'
```

Luego mirar **para qué** se usa el valor: una animación o un color no importan; un token sí.

## Impacto en A/D

- **auth-bypass**: predecir el token de sesión o el código de reset del usuario del checker.
- **flag-leak**: predecir el ID "secreto" de una nota o el nombre de archivo de un flag.
- **Crypto rota**: claves privadas o nonces predecibles (ver [Crypto](../Crypto/overview.md)).

## Referencias

- [OWASP: Insecure Randomness](https://owasp.org/www-community/vulnerabilities/Insecure_Randomness)
- [randcrack](https://github.com/tna0y/Python-random-module-cracker)
- [CWE-338](https://cwe.mitre.org/data/definitions/338.html)

# Parche: Input Validation

## Estrategia

Validar **en el servidor**, **lo más cerca posible del uso**, con **allowlist** (qué es válido) en vez de blacklist (qué es malo). Para cada campo: tipo, longitud, formato y rango.

### 1. Números

- Convertir al tipo correcto y rechazar si falla.
- Rango explícito: `0 < amount <= MAX`.
- Rechazar `NaN` e `Infinity` (en Python y JS **todas** las comparaciones con `NaN` dan `false`, así que `if amount <= 0: reject` deja pasar `NaN`).
- Dinero: enteros (centavos) o `Decimal`, nunca `float`.
- Multiplicaciones: verificar overflow (`Math.multiplyExact` en Java, límites antes de multiplicar en Go/C).
- Operaciones de saldo: **atómicas** (`UPDATE ... SET balance = balance - ? WHERE id = ? AND balance >= ?`) para evitar race conditions.

### 2. Mass assignment

- Copiar solo los campos permitidos (`{k: data[k] for k in ALLOWED}`), o usar DTOs/structs de entrada sin campos sensibles.
- Campos como `is_admin`, `role`, `owner_id`, `balance`, `id` nunca vienen del cliente.

### 3. Regex

| Lenguaje | Correcto | Trampa |
|---|---|---|
| Python | `re.fullmatch(r"[a-z]{1,32}", x)` | `re.match(r"^[a-z]+$", x)` acepta `"abc\n"` |
| PHP | `preg_match('/\A[a-z]{1,32}\z/', $x)` o modificador `D` | `/^[a-z]+$/` acepta `"abc\n"` |
| Ruby | `x.match?(/\A[a-z]{1,32}\z/)` | `^`/`$` son por línea: `"abc\nX"` pasa |
| JS | `/^[a-z]{1,32}$/.test(x)` | flag `g` con `.test()` guarda `lastIndex` → resultados alternados |
| Java | `x.matches("[a-z]{1,32}")` | `Pattern.compile(...).matcher(x).find()` busca subcadenas |
| Go | `regexp.MustCompile(`^[a-z]{1,32}$`)` | sin `^...$`, `MatchString` busca subcadenas |

### 4. Tipos

- JSON: verificar el tipo de cada campo (`isinstance(x, int) and not isinstance(x, bool)` en Python: `True` es un `int`).
- Express/PHP: `?x[]=1` llega como array → `typeof x === 'string'` / `is_string($x)`.
- Booleanos: comparar con el valor exacto (`x === true`), no por truthiness (`"false"` es truthy).

### 5. Saltos de línea y caracteres de control

- Rechazar `\r`, `\n`, `\0` y otros controles en campos de una línea (usernames, títulos), sobre todo si se guardan en archivos de texto o viajan por un protocolo TCP por líneas.
- Logs: escapar `\r\n` o loguear en JSON.

### 6. Unicode y mayúsculas

- Normalizar antes de validar y antes de comparar unicidad: `unicodedata.normalize("NFKC", s).casefold()`.
- O allowlist ASCII estricta para identificadores.

### 7. Longitud y ReDoS

- Límite de longitud en todos los campos **antes** de aplicar regex o procesar.
- Evitar cuantificadores anidados (`(a+)+`, `(a|aa)*`, `(.*a){10}`). Go (RE2) es inmune; Python, JS, Java y PHP no.

## Errores comunes

- Validar solo en el frontend (HTML `min="0"`, `maxlength`): el atacante usa `curl`.
- Validar un campo y usar otro: validar `request.args["user"]` y usar `request.values["user"]`; validar el primer `?user=` y que el framework use el último.
- Validar antes de decodificar/normalizar y usar el valor después.
- Validaciones más estrictas que lo que envía el checker: revisar el tráfico del checker antes de restringir formatos (largo de usernames, caracteres permitidos).
- Responder con un código/formato distinto al rechazar un input que el checker sí envía: el servicio queda en *mumble*.

## Defensa en profundidad

- Constraints en la base de datos (`CHECK (balance >= 0)`, `UNIQUE`, `NOT NULL`, largos de columna).
- Librerías de schemas si ya están en la imagen: pydantic, marshmallow, joi/zod, Bean Validation (`@Min`, `@Size`), `go-playground/validator`.

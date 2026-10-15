# Memory Corruption (C/C++)

## Qué es

Errores de manejo de memoria en servicios escritos en C/C++ que permiten leer o escribir fuera de los límites de un buffer. En A/D casi nunca hace falta un exploit completo de RCE: basta con **pisar una variable vecina** (`logged_in`, `is_admin`, `user_id`, un puntero a la nota) o **leer** memoria con el flag.

| Bug | Ejemplo | Consecuencia típica |
|---|---|---|
| Copia sin límite | `strcpy`, `strcat`, `sprintf`, `gets`, `scanf("%s")` | Overflow en stack/bss |
| Format string | `printf(user)` | Leer el stack (`%p %s`), escribir con `%n` |
| `char` con signo en `%x` (stldoctor) | `sprintf(bp, "%02x", c)` con `c >= 0x80` → `ffffff80` | Escribe 8 chars en vez de 2 → overflow |
| `char` vs `EOF` (stldoctor) | `char c = fgetc(f); while (c != EOF)` | El byte `0xff` corta la lectura: controlar campos siguientes |
| Longitud del atacante (stldoctor) | `strncmp(a, b, strlen(a))` | Input vacío o prefijo coinciden → auth-bypass |
| Overflow de enteros (stldoctor) | `malloc(n * size)` | Buffer chico + escritura grande |
| Off-by-one | `buf[len] = 0` con `len == sizeof buf` | Pisa un byte (a veces el LSB de un puntero o un flag) |
| Longitud con signo | `int len; if (len > MAX)...; memcpy(d, s, len)` con `len < 0` | Copia gigante |
| Use-after-free / double free | `free(p)` y después usar `p` | Corrupción del heap |
| Variable sin inicializar | `char buf[64]; send(buf, 64)` | Filtra datos de otra sesión |

## Cómo identificarla en código

```bash
rg -n '\b(strcpy|strcat|sprintf|vsprintf|gets|scanf\("%s")\b'
rg -n 'printf\(\s*[a-z_]+\s*\)|fprintf\(\s*\w+\s*,\s*[a-z_]+\s*\)'
rg -n 'malloc\([^)]*\*|realloc\([^)]*\*'
rg -n '\b(fgetc|getc|getchar)\('
rg -n 'strncmp\([^,]+,[^,]+,\s*strlen'
rg -n 'read\(\s*\w+\s*,\s*\w+\s*,\s*0x'
```

Después: ubicar las variables de estado de auth (`nm -n binario`, structs) y ver **qué buffer está justo antes**.

## Impacto en A/D

- **auth-bypass** pisando un flag de sesión.
- **flag-leak** con format string o lecturas fuera de límites.
- **RCE** en los casos clásicos (stack overflow sin canario, `%n`).

## Referencias

- [SEI CERT C Coding Standard](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard)
- [CWE-787](https://cwe.mitre.org/data/definitions/787.html), [CWE-134](https://cwe.mitre.org/data/definitions/134.html), [CWE-190](https://cwe.mitre.org/data/definitions/190.html), [CWE-197](https://cwe.mitre.org/data/definitions/197.html)

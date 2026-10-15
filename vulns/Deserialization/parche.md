# Parche: Insecure Deserialization

## Estrategia

1. **Cambiar a un formato de datos puros**: JSON (`json.loads`, `JSON.parse`, `json_decode`, Jackson sin default typing, `System.Text.Json`).
2. Si el formato no se puede cambiar (hay datos ya guardados que el checker va a leer): **restringir las clases** permitidas.
3. Si el blob viaja al cliente: **firmarlo con HMAC** usando un secreto propio (no el del código) y verificar la firma **antes** de deserializar.

| Lenguaje | Parche mínimo |
|---|---|
| Python | `json.loads`; `yaml.safe_load`; pickle con `Unpickler.find_class` restringido |
| PHP | `json_decode`; `unserialize($x, ['allowed_classes' => false])` |
| Java | JSON DTOs; `ObjectInputFilter` con allowlist (Java 9+) |
| Node | `JSON.parse`; eliminar `node-serialize` |
| Ruby | `JSON.parse`; `YAML.safe_load`; nunca `Marshal.load` con datos externos |
| .NET | `System.Text.Json`; `TypeNameHandling.None` |

## Errores comunes

- Cambiar el formato de escritura y de lectura a la vez cuando ya hay datos guardados en el formato viejo → el checker no recupera flags de rondas anteriores. Leer ambos formatos durante la transición o migrar los datos existentes.
- Blacklist de clases (`os`, `subprocess`, `Runtime`): siempre aparece otro gadget.
- Verificar la firma con `==` (timing) o con el secreto hardcodeado que todos conocen.
- `yaml.load(x, Loader=yaml.Loader)` o `FullLoader` en versiones viejas de PyYAML: siguen siendo inseguros. Usar `SafeLoader`.

## Defensa en profundidad

- Tratar todo blob serializado que venga del cliente como input no confiable, aunque esté en base64 o "cifrado".
- Mantener sesiones del lado del servidor (Redis/DB) y enviar al cliente solo un ID aleatorio.

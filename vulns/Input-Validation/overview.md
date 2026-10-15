# Input Validation (validación de entrada general)

## Qué es

Fallas en cómo el servicio valida los datos que recibe, **independientes del sink** (SQL, shell, archivo). No inyectan código: rompen la lógica de negocio o el formato de almacenamiento. Son muy comunes en A/D porque los scanners casi no las detectan.

| Bug | Ejemplo | Consecuencia típica |
|---|---|---|
| Números sin límites | `transfer(amount=-1000)`, `qty=1e309`, `amount=NaN` | Saldo infinito, comprar el flag sin pagar |
| Overflow numérico | `price * qty` desborda `int32`/`int64` | Total negativo o cero |
| Mass assignment | `User(**request.json)` con `{"is_admin": true}` | Escalar a admin, cambiar el dueño de una nota |
| Anclas de regex | Python/PHP `^[a-z]+$` acepta `"abc\n"`; Ruby `^...$` valida por línea | Saltar la validación con un salto de línea |
| Regex sin anclar | `re.search(r"[a-z]+", x)` / `regex.MatchString` | Cualquier string que *contenga* algo válido pasa |
| Confusión de tipos | `?id[]=1` (array), `{"amount": "10"}` (string), `{"admin": "false"}` (string truthy) | Comparaciones que dan `true` inesperadamente |
| Inyección de saltos de línea | `\n` en un username guardado en un archivo línea por línea, o en un protocolo TCP por líneas | Crear registros/comandos extra (`alice\nadmin:1`) |
| CRLF / log injection | `\r\n` en headers, redirects o logs | Header injection, logs falsos |
| Normalización Unicode | `ａｄｍｉｎ` (fullwidth) o `Admin` vs `admin` | Registrar un usuario que colisiona con otro |
| Longitud sin límite | username de 10 MB | DoS, overflow en servicios C |
| ReDoS | `^(a+)+$` con `"aaaa…!"` | Un request bloquea un worker → SLA caído |
| Parameter pollution | `?user=alice&user=admin` | Validar un valor y usar el otro |

## Cómo identificarla en código

```bash
# Numeros
rg -n 'float\(|int\(|parseInt|parseFloat|Number\(|Atoi|ParseInt|parseInt\(|intval|floatval'
rg -n -i 'amount|balance|price|qty|quantity|credits|points'
# Mass assignment
rg -n '\*\*request\.(json|form)|__dict__\.update|Object\.assign\(.*req\.body|\.\.\.req\.body|->fill\(\$_|json\.Unmarshal\(.*&(user|model)'
# Regex
rg -n 're\.(match|search)\(|preg_match\(|\.test\(|MatchString\(|=~'
# Almacenamiento por lineas
rg -n 'write\(.*\\n|fprintf\(.*\\n|appendFile|file_put_contents\(.*FILE_APPEND'
```

## Impacto en A/D

- **flag-leak / auth-bypass** cuando el flag es un "premio" (comprarlo con créditos, ser admin, nivel VIP).
- **integrity**: crear usuarios o registros falsos en archivos de texto.
- **dos**: ReDoS o inputs gigantes contra tu propio servicio.

## Referencias

- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [OWASP Mass Assignment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html)
- [OWASP ReDoS](https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS)
- [CWE-20](https://cwe.mitre.org/data/definitions/20.html), [CWE-915](https://cwe.mitre.org/data/definitions/915.html), [CWE-1333](https://cwe.mitre.org/data/definitions/1333.html), [CWE-93](https://cwe.mitre.org/data/definitions/93.html)

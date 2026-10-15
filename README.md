# Patching_Guide_CR_CTF
Este repositorio tiene como objetivo centralizar parches de diferentes vulnerabilidades conocidas con sus respectivos parches en diferentes lenguajes, esto con el propósito de ser una fuente de información centralizada para el proceso de patching en entornos de Attack and Defense (AD).

## Cómo navegar

El repo está organizado por vulnerabilidad bajo la carpeta `vulns/`. Cada vuln tiene la misma estructura:

- **`overview.md`** — qué es la vuln, cómo identificarla en código, impacto y referencias.
- **`parche.md`** — estrategia general de patching, errores comunes y recomendaciones de defensa en profundidad.
- **`samples/<lenguaje>/`** — pares `vulnerable.<ext>` y `parchado.<ext>` listos para comparar lado a lado.

Para una referencia rápida durante el juego (workflow, triage y cheatsheet por lenguaje), ver **[PATCHERS_GUIDE.md](PATCHERS_GUIDE.md)**.

## Índice de vulnerabiidades

<!-- AUTO-INDEX:START -->
<!-- Esta sección se genera automáticamente. No la edites a mano. -->

| Vulnerabilidad | Lenguajes cubiertos | Docs |
|---|---|---|
| Command Injection | [C](vulns/Command-Injection/samples/C/), [go](vulns/Command-Injection/samples/go/), [java](vulns/Command-Injection/samples/java/), [js](vulns/Command-Injection/samples/js/), [php](vulns/Command-Injection/samples/php/), [python](vulns/Command-Injection/samples/python/), [ruby](vulns/Command-Injection/samples/ruby/) | [Overview](vulns/Command-Injection/overview.md) · [Parche](vulns/Command-Injection/parche.md) |
| Crypto | [C](vulns/Crypto/samples/C/), [JS](vulns/Crypto/samples/JS/), [python](vulns/Crypto/samples/python/) | [Overview](vulns/Crypto/overview.md) · [Parche](vulns/Crypto/parche.md) |
| Insecure Deserialization | [csharp](vulns/Deserialization/samples/csharp/), [java](vulns/Deserialization/samples/java/), [js](vulns/Deserialization/samples/js/), [php](vulns/Deserialization/samples/php/), [python](vulns/Deserialization/samples/python/), [ruby](vulns/Deserialization/samples/ruby/) | [Overview](vulns/Deserialization/overview.md) · [Parche](vulns/Deserialization/parche.md) |
| IDOR (Insecure Direct Object Reference) | [C](vulns/IDOR/samples/C/), [go](vulns/IDOR/samples/go/), [java](vulns/IDOR/samples/java/), [js](vulns/IDOR/samples/js/), [php](vulns/IDOR/samples/php/), [python](vulns/IDOR/samples/python/) | [Overview](vulns/IDOR/overview.md) · [Parche](vulns/IDOR/parche.md) |
| Input Validation (validación de entrada general) | [go](vulns/Input-Validation/samples/go/), [java](vulns/Input-Validation/samples/java/), [js](vulns/Input-Validation/samples/js/), [php](vulns/Input-Validation/samples/php/), [python](vulns/Input-Validation/samples/python/) | [Overview](vulns/Input-Validation/overview.md) · [Parche](vulns/Input-Validation/parche.md) |
| Memory Corruption (C/C++) | [C](vulns/Memory-Corruption/samples/C/) | [Overview](vulns/Memory-Corruption/overview.md) · [Parche](vulns/Memory-Corruption/parche.md) |
| NoSQL Injection | [js](vulns/NoSQLi/samples/js/), [php](vulns/NoSQLi/samples/php/), [python](vulns/NoSQLi/samples/python/) | [Overview](vulns/NoSQLi/overview.md) · [Parche](vulns/NoSQLi/parche.md) |
| Path Traversal | [C](vulns/Path-Traversal/samples/C/), [csharp](vulns/Path-Traversal/samples/csharp/), [go](vulns/Path-Traversal/samples/go/), [java](vulns/Path-Traversal/samples/java/), [js](vulns/Path-Traversal/samples/js/), [php](vulns/Path-Traversal/samples/php/), [python](vulns/Path-Traversal/samples/python/) | [Overview](vulns/Path-Traversal/overview.md) · [Parche](vulns/Path-Traversal/parche.md) |
| SQL Injection | [C](vulns/SQLi/samples/C/), [csharp](vulns/SQLi/samples/csharp/), [go](vulns/SQLi/samples/go/), [java](vulns/SQLi/samples/java/), [js](vulns/SQLi/samples/js/), [php](vulns/SQLi/samples/php/), [python](vulns/SQLi/samples/python/), [ruby](vulns/SQLi/samples/ruby/) | [Overview](vulns/SQLi/overview.md) · [Parche](vulns/SQLi/parche.md) |
| SSRF (Server-Side Request Forgery) | [go](vulns/SSRF/samples/go/), [js](vulns/SSRF/samples/js/), [php](vulns/SSRF/samples/php/), [python](vulns/SSRF/samples/python/) | [Overview](vulns/SSRF/overview.md) · [Parche](vulns/SSRF/parche.md) |
| SSTI (Server-Side Template Injection) | [go](vulns/SSTI/samples/go/), [java](vulns/SSTI/samples/java/), [js](vulns/SSTI/samples/js/), [php](vulns/SSTI/samples/php/), [python](vulns/SSTI/samples/python/) | [Overview](vulns/SSTI/overview.md) · [Parche](vulns/SSTI/parche.md) |
| Secretos hardcodeados, sesiones y JWT | [go](vulns/Secrets-JWT/samples/go/), [java](vulns/Secrets-JWT/samples/java/), [js](vulns/Secrets-JWT/samples/js/), [php](vulns/Secrets-JWT/samples/php/), [python](vulns/Secrets-JWT/samples/python/) | [Overview](vulns/Secrets-JWT/overview.md) · [Parche](vulns/Secrets-JWT/parche.md) |
| Aleatoriedad débil (Weak Randomness) | [C](vulns/Weak-Randomness/samples/C/), [go](vulns/Weak-Randomness/samples/go/), [java](vulns/Weak-Randomness/samples/java/), [js](vulns/Weak-Randomness/samples/js/), [php](vulns/Weak-Randomness/samples/php/), [python](vulns/Weak-Randomness/samples/python/) | [Overview](vulns/Weak-Randomness/overview.md) · [Parche](vulns/Weak-Randomness/parche.md) |
| XSS (Cross-Site Scripting) | [go](vulns/XSS/samples/go/), [js](vulns/XSS/samples/js/), [php](vulns/XSS/samples/php/), [python](vulns/XSS/samples/python/) | [Overview](vulns/XSS/overview.md) · [Parche](vulns/XSS/parche.md) |
| XXE (XML External Entity) | [csharp](vulns/XXE/samples/csharp/), [java](vulns/XXE/samples/java/), [php](vulns/XXE/samples/php/), [python](vulns/XXE/samples/python/) | [Overview](vulns/XXE/overview.md) · [Parche](vulns/XXE/parche.md) |

<!-- AUTO-INDEX:END -->
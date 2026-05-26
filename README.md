# Patching_Guide_CR_CTF
Este repositorio tiene como objetivo centralizar parches de diferentes vulnerabilidades conocidas con sus respectivos parches en diferentes lenguajes, esto con el propósito de ser una fuente de información centralizada para el proceso de patching en entornos de Attack and Defense (AD).

## Cómo navegar

El repo está organizado por vulnerabilidad bajo la carpeta `vulns/`. Cada vuln tiene la misma estructura:

- **`overview.md`** — qué es la vuln, cómo identificarla en código, impacto y referencias.
- **`parche.md`** — estrategia general de patching, errores comunes y recomendaciones de defensa en profundidad.
- **`samples/<lenguaje>/`** — pares `vulnerable.<ext>` y `parchado.<ext>` listos para comparar lado a lado.

## Índice de vulnerabiidades

<!-- AUTO-INDEX:START -->
<!-- Esta sección se genera automáticamente. No la edites a mano. -->

| Vulnerabilidad | Lenguajes cubiertos | Docs |
|---|---|---|
| IDOR | [C](vulns/IDOR/samples/C/) | [Overview](vulns/IDOR/overview.md) |
| SQLi | [C](vulns/SQLi/samples/C/), [python](vulns/SQLi/samples/python/) | [Overview](vulns/SQLi/overview.md) · [Parche](vulns/SQLi/parche.md) |

<!-- AUTO-INDEX:END -->
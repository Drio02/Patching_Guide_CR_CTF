# XSS (Cross-Site Scripting)

## Qué es

El servicio inserta input del usuario en una página HTML sin escaparlo, y el navegador de otra persona ejecuta el JavaScript inyectado.

- **Reflejado**: el payload viaja en la URL y se devuelve en la misma respuesta.
- **Almacenado**: el payload se guarda (nota, perfil, comentario) y se ejecuta para cada visitante.
- **DOM-based**: el JavaScript del frontend escribe datos en el DOM con `innerHTML`, `document.write`, `eval`.

## Cómo identificarla en código

| Stack | Escapa por defecto | Bypass a buscar |
|---|---|---|
| Jinja2 / Flask | sí (`.html`) | `\|safe`, `Markup()`, `{% autoescape false %}`, `render_template_string` |
| EJS | `<%= %>` sí | `<%- %>` |
| Handlebars | `{{ }}` sí | `{{{ }}}` |
| Twig | sí | `\|raw` |
| PHP plano | **no** | `echo $x` |
| Go | `html/template` sí | `text/template` para HTML, `template.HTML(x)` |
| React / Vue | sí | `dangerouslySetInnerHTML`, `v-html` |
| Frontend | — | `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `$(x).html()` |

```bash
rg -n 'innerHTML|outerHTML|insertAdjacentHTML|document\.write|\.html\(|\|\s*safe|\|raw|Markup\(|<%-|\{\{\{|dangerouslySetInnerHTML|v-html|template\.HTML\('
```

## Impacto en A/D

Solo relevante si el juego tiene un **bot** que visita páginas (un "admin" que revisa reportes, un checker con navegador headless). En ese caso: **session-theft** → robar la cookie del bot o hacer acciones como él (leer sus notas con flag). Si no hay bot, prioridad baja.

## Referencias

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP DOM based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
- [CWE-79](https://cwe.mitre.org/data/definitions/79.html)

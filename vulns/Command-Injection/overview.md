# Command Injection

## Qué es

El servicio ejecuta un comando del sistema construido con input del usuario y lo pasa a una **shell** (`sh -c`). Los metacaracteres de la shell (`;`, `|`, `&&`, `` ` ``, `$()`, saltos de línea) permiten encadenar comandos arbitrarios: `127.0.0.1; cat /data/flags/*`.

Variante relacionada: **argument injection**. Sin shell, pero el valor empieza con `-` y se interpreta como opción del programa (`--output=/app/x`, `-oProxyCommand=...` en ssh, `--upload-pack` en git, `-exec` en find).

## Cómo identificarla en código

| Lenguaje | Sinks con shell |
|---|---|
| Python | `os.system`, `os.popen`, `subprocess.*(..., shell=True)`, `commands.getoutput` |
| Node | `child_process.exec`, `execSync`, `spawn(..., {shell: true})` |
| PHP | `system`, `exec`, `shell_exec`, `passthru`, `popen`, `proc_open`, backticks |
| Java | `Runtime.exec("sh -c ...")`, `ProcessBuilder("sh", "-c", ...)` |
| Go | `exec.Command("sh", "-c", ...)`, `exec.Command("bash", "-c", ...)` |
| Ruby | backticks, `%x()`, `system("string")`, `exec("string")`, `IO.popen("string")`, `Open3` con string |
| C | `system()`, `popen()` |

```bash
rg -n 'os\.system|os\.popen|shell=True|child_process|execSync|\bexec\(|shell_exec|passthru|popen|proc_open|Runtime\.getRuntime|"sh", "-c"|"bash", "-c"|%x\(|\bsystem\('
```

## Impacto en A/D

- **RCE**: leer todos los flags, de todos los servicios que corren con el mismo usuario.
- El atacante puede borrar tus datos, dejar un backdoor o tirar el servicio (SLA). Prioridad máxima.

## Referencias

- [OWASP OS Command Injection Defense Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)
- [CWE-78](https://cwe.mitre.org/data/definitions/78.html), [CWE-88](https://cwe.mitre.org/data/definitions/88.html)
- [GTFOArgs](https://gtfoargs.github.io/) (argument injection por binario)

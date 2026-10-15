# Parche: SSRF

## Estrategia

1. Si el feature solo necesita **un host conocido**: hardcodearlo y no aceptar URLs del usuario.
2. Si no: **allowlist de esquema** (`http`, `https`), **resolver el host** y **rechazar IPs privadas/loopback/link-local/reservadas** (incluyendo IPv6 y IPv4-mapped).
3. **Desactivar redirects** (o validar cada salto): un servidor externo puede redirigir a `127.0.0.1`.
4. Conectarse **a la IP ya validada** para evitar DNS rebinding (resolver una vez y usar esa IP).
5. `timeout` siempre.

## Errores comunes

- Blacklist de strings (`"localhost"`, `"127.0.0.1"`): se bypassea con `127.1`, `0`, `0x7f000001`, `2130706433`, `[::1]`, `localtest.me`, nombres de contenedores (`db`, `redis`).
- Validar el host con `urlparse` y pedir con otra librería que parsea distinto (`http://evil.com#@127.0.0.1`).
- Olvidar redirects (`requests` los sigue por defecto).
- Validar el DNS y después dejar que la librería resuelva de nuevo (DNS rebinding con TTL 0).
- Olvidar que los **nombres de servicios de Docker** resuelven a IPs privadas `172.16.0.0/12`: la verificación de IP privada los cubre; la blacklist de strings no.

## Defensa en profundidad

- Los endpoints internos deben exigir autenticación aunque vengan de `127.0.0.1`.
- Redes de Docker separadas: el servicio web no necesita ver Redis de otro servicio.

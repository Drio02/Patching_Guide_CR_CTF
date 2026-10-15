# Insecure Deserialization

## Qué es

El servicio reconstruye objetos a partir de bytes controlados por el usuario usando un formato que puede **instanciar clases arbitrarias o ejecutar código** durante la deserialización (`pickle`, `unserialize`, `ObjectInputStream`, `Marshal`, `BinaryFormatter`, YAML no seguro). El atacante envía un objeto preparado y obtiene ejecución de código o modifica el estado (p. ej. `is_admin = true`).

Lugares típicos en A/D: cookies de sesión "caseras", campos ocultos, archivos importados/subidos, caché en Redis, mensajes entre microservicios.

## Cómo identificarla en código

| Lenguaje | Sink peligroso |
|---|---|
| Python | `pickle.loads`, `cPickle`, `dill`, `shelve`, `jsonpickle.decode`, `yaml.load` sin `SafeLoader`, `yaml.unsafe_load`, `numpy.load(allow_pickle=True)`, `torch.load` |
| PHP | `unserialize($user)`, `phar://` en funciones de archivo (`file_exists`, `fopen`) |
| Java | `ObjectInputStream.readObject`, `XMLDecoder`, XStream, Jackson con default typing, SnakeYAML `new Yaml().load` |
| Node | `node-serialize.unserialize`, `funcster`, `eval`/`Function` sobre datos |
| Ruby | `Marshal.load`, `YAML.load` (Psych < 4), `Oj.load` en modo object |
| .NET | `BinaryFormatter`, `NetDataContractSerializer`, `LosFormatter`, Json.NET con `TypeNameHandling` ≠ `None` |

```bash
rg -n 'pickle\.loads?|jsonpickle|yaml\.load\(|unsafe_load|unserialize\(|ObjectInputStream|readObject|XMLDecoder|Marshal\.load|BinaryFormatter|TypeNameHandling|node-serialize'
rg -n 'base64.*(loads|unserialize)|b64decode.*pickle'
```

## Impacto en A/D

- **RCE** en casi todos los casos (gadget chains, `__reduce__` en pickle).
- Si la cookie está firmada con un secreto hardcodeado, cualquier equipo puede firmar un pickle malicioso.

## Referencias

- [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
- [ysoserial](https://github.com/frohoff/ysoserial), [PHPGGC](https://github.com/ambionics/phpggc)
- [CWE-502](https://cwe.mitre.org/data/definitions/502.html)

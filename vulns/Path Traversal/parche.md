La idea central es nunca confiar en la ruta que arma el usuario. Las defensas principales:

Resolver la ruta canónica (eliminar `..`, symlinks, etc.) y verificar que el resultado quede dentro del directorio permitido. Esta es la defensa más robusta.
Validar/sanitizar el input: aceptar solo nombres de archivo (sin separadores de ruta), idealmente con una allowlist o una regex restrictiva.
Usar solo el nombre base del archivo (`basename`) descartando cualquier componente de directorio.
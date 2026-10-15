<?php
$base = '/var/www/uploads';

// Vuln 1: lectura directa
echo file_get_contents($base . '/' . $_GET['file']);      // ?file=../../../etc/passwd

// Vuln 2: LFI, include con input del usuario
include 'pages/' . $_GET['page'] . '.php';
// ?page=../../../../tmp/sess_xxx (sesion envenenada) o php://filter/convert.base64-encode/resource=config

// Vuln 3: filtro de una sola pasada
$f = str_replace('../', '', $_GET['f']);                   // ....// -> ../
readfile($base . '/' . $f);

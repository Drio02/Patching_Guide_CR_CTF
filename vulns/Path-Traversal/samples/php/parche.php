<?php
$base = realpath('/var/www/uploads');

// Patch 1: realpath + verificar prefijo con separador (PHP 8)
function safe_path(string $base, string $name): string {
    $real = realpath($base . DIRECTORY_SEPARATOR . $name);
    // realpath devuelve false si el archivo no existe
    if ($real === false || !str_starts_with($real, $base . DIRECTORY_SEPARATOR)) {
        http_response_code(403);
        exit;
    }
    return $real;
}
echo file_get_contents(safe_path($base, $_GET['file']));

// Patch 2: LFI -> allowlist de paginas, el usuario nunca controla la ruta
$pages = ['home' => 'pages/home.php', 'about' => 'pages/about.php'];
include $pages[$_GET['page'] ?? 'home'] ?? 'pages/home.php';

// Patch 3: basename descarta directorios + regex
$f = basename($_GET['f']);
if (!preg_match('/^[A-Za-z0-9_-]{1,64}$/', $f)) { http_response_code(400); exit; }
readfile($base . '/' . $f);

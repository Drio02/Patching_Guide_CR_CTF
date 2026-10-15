<?php
// Patch 1 (preferido): JSON
$prefs = json_decode(base64_decode($_COOKIE['prefs'] ?? ''), true) ?? [];

// Patch 1b: si hay que mantener unserialize, sin objetos
$prefs = unserialize(base64_decode($_COOKIE['prefs'] ?? ''), ['allowed_classes' => false]);

// Patch 2: no aceptar wrappers en rutas del usuario (phar://, php://, etc.)
$path = $_GET['path'] ?? '';
if (preg_match('#^[a-z0-9]+://#i', $path)) { http_response_code(400); exit; }
if (file_exists('uploads/' . basename($path))) { echo "exists"; }
// PHP 8: phar:// ya no deserializa la metadata automaticamente

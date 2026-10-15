<?php
// Patch 1: validar IP + escapeshellarg
$host = $_POST['host'] ?? '';
if (!filter_var($host, FILTER_VALIDATE_IP)) { http_response_code(400); exit; }
echo shell_exec('ping -c 1 ' . escapeshellarg($host));

// Patch 2: no hace falta un subproceso para contar lineas
$file = basename($_GET['file'] ?? '');
if (!preg_match('/^[A-Za-z0-9_-]{1,64}\.txt$/', $file)) { http_response_code(400); exit; }
echo count(file('uploads/' . $file));

// Patch 3: usar la extension curl de PHP en vez del binario
$url = $_GET['url'] ?? '';
if (!preg_match('#^https?://#', $url)) { http_response_code(400); exit; }
$ch = curl_init($url);
curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 5,
                        CURLOPT_PROTOCOLS => CURLPROTO_HTTP | CURLPROTO_HTTPS]);
echo curl_exec($ch);

// PHP 7.4+: proc_open acepta un array y no usa shell
// $p = proc_open(['ping', '-c', '1', $host], [1 => ['pipe', 'w']], $pipes);

<?php
// Devuelve la IP validada (o termina con 403)
function check_url(string $url): array {
    $p = parse_url($url);
    if (!$p || !in_array($p['scheme'] ?? '', ['http', 'https'], true) || empty($p['host'])) {
        http_response_code(400); exit;
    }
    $host = trim($p['host'], '[]');
    $ips = filter_var($host, FILTER_VALIDATE_IP) ? [$host] : gethostbynamel($host);
    if (!$ips) { http_response_code(400); exit; }
    foreach ($ips as $ip) {
        // NO_PRIV_RANGE + NO_RES_RANGE rechazan 10/8, 172.16/12, 192.168/16, 127/8, 0/8, 169.254/16, etc.
        if (!filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE)) {
            http_response_code(403); exit;
        }
    }
    $port = $p['port'] ?? (($p['scheme'] === 'https') ? 443 : 80);
    return [$host, $port, $ips[0]];
}

// Patch: solo http/https, IP validada, sin redirects, conexion fijada a esa IP (anti DNS rebinding)
$url = $_POST['url'] ?? '';
[$host, $port, $ip] = check_url($url);
$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_FOLLOWLOCATION => false,
    CURLOPT_PROTOCOLS      => CURLPROTO_HTTP | CURLPROTO_HTTPS,
    CURLOPT_TIMEOUT        => 5,
    CURLOPT_RESOLVE        => ["$host:$port:$ip"],
]);
echo curl_exec($ch);

// Y nunca file_get_contents() con URLs del usuario.

<?php
// Patch 1: mismo formato (32 hex) con CSPRNG
$session_token = bin2hex(random_bytes(16));

// Patch 2
$reset_code = random_int(100000, 999999);

// Patch 3: mismo alfabeto y largo
function rand_str(int $len, string $cs = 'abcdefghijklmnopqrstuvwxyz0123456789'): string {
    $out = '';
    for ($i = 0; $i < $len; $i++) $out .= $cs[random_int(0, strlen($cs) - 1)];
    return $out;
}
$note_id = rand_str(16);

<?php
// Patch 1: secreto aleatorio persistido fuera del webroot
function secret(): string {
    $f = '/data/hmac.key';
    if (!file_exists($f)) file_put_contents($f, bin2hex(random_bytes(32)));
    return trim(file_get_contents($f));
}

function check_cookie(): ?string {
    $parts = explode('|', $_COOKIE['auth'] ?? '');
    if (count($parts) !== 2) return null;
    [$user, $sig] = $parts;
    // Patch 2: HMAC-SHA256 (sin length extension)
    // Patch 3: hash_equals, estricta y de tiempo constante
    if (hash_equals(hash_hmac('sha256', $user, secret()), $sig)) return $user;
    return null;
}

function make_cookie(string $user): string {
    return $user . '|' . hash_hmac('sha256', $user, secret());
}

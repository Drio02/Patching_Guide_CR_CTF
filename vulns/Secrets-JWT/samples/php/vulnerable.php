<?php
// Cookie "firmada" a mano con un secreto hardcodeado
const SECRET = 'changeme';

function check_cookie(): ?string {
    [$user, $sig] = explode('|', $_COOKIE['auth'] ?? '|');
    // Vuln 1: secreto publico (todos tienen el codigo)
    // Vuln 2: md5(secret . data) -> length extension
    // Vuln 3: == es comparacion floja y no es de tiempo constante ("0e..." == "0e...")
    if (md5(SECRET . $user) == $sig) return $user;
    return null;
}

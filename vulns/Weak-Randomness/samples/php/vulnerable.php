<?php
// Vuln 1: uniqid es la hora en microsegundos
$session_token = md5(uniqid());

// Vuln 2: mt_rand recuperable con unas pocas salidas (php_mt_seed)
$reset_code = mt_rand(100000, 999999);

// Vuln 3: str_shuffle usa el mismo PRNG
$note_id = substr(str_shuffle('abcdefghijklmnopqrstuvwxyz0123456789'), 0, 16);

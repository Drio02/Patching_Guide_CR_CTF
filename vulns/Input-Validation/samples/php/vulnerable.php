<?php
session_start();

// Vuln 1: intval acepta negativos; "10abc" -> 10; floatval("1e999") -> INF
$amount = intval($_POST['amount']);                 // -1000
$stmt = $pdo->prepare("UPDATE accounts SET balance = balance - ? WHERE user = ?");
$stmt->execute([$amount, $_SESSION['user']]);
$stmt = $pdo->prepare("UPDATE accounts SET balance = balance + ? WHERE user = ?");
$stmt->execute([$amount, $_POST['to']]);

// Vuln 2: $ en PCRE acepta un "\n" final
if (!preg_match('/^[a-z0-9_]+$/', $_POST['username'])) die('bad username');
// username = "eve\n" pasa; si se guarda en un archivo por lineas, rompe el formato

// Vuln 3: mass assignment, cada campo del POST se copia al objeto
$user = load_user($_SESSION['user']);
foreach ($_POST as $k => $v) { $user->$k = $v; }   // role=admin
save_user($user);

// Vuln 4: archivo por lineas sin filtrar saltos de linea
file_put_contents('/data/users.txt', $_POST['username'] . ':' . $_POST['password'] . ":0\n", FILE_APPEND);
// password = "x:0\nadmin2:pw:1"  -> crea un usuario admin

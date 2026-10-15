<?php
session_start();

// Patch 1: filter_var con rango + descuento condicionado al saldo
$amount = filter_var($_POST['amount'] ?? null, FILTER_VALIDATE_INT,
                     ['options' => ['min_range' => 1, 'max_range' => 1000000]]);
if ($amount === false) { http_response_code(400); exit; }

$pdo->beginTransaction();
$stmt = $pdo->prepare("UPDATE accounts SET balance = balance - ? WHERE user = ? AND balance >= ?");
$stmt->execute([$amount, $_SESSION['user'], $amount]);
if ($stmt->rowCount() !== 1) { $pdo->rollBack(); http_response_code(400); exit('insufficient funds'); }
$stmt = $pdo->prepare("UPDATE accounts SET balance = balance + ? WHERE user = ?");
$stmt->execute([$amount, $_POST['to']]);
$pdo->commit();

// Patch 2: \A ... \z (o modificador D) y longitud en el patron
$username = $_POST['username'] ?? '';
if (!is_string($username) || !preg_match('/\A[a-z0-9_]{3,32}\z/', $username)) {
    http_response_code(400); exit('bad username');
}

// Patch 3: allowlist de campos editables
$user = load_user($_SESSION['user']);
foreach (['display_name', 'bio'] as $k) {
    if (isset($_POST[$k]) && is_string($_POST[$k]) && strlen($_POST[$k]) <= 200) {
        $user->$k = $_POST[$k];
    }
}
save_user($user);

// Patch 4: rechazar separadores y caracteres de control en campos que van a un archivo por lineas
$password = $_POST['password'] ?? '';
if (!is_string($password) || preg_match('/[\x00-\x1f:]/', $password) || strlen($password) > 128) {
    http_response_code(400); exit;
}
file_put_contents('/data/users.txt', "$username:$password:0\n", FILE_APPEND | LOCK_EX);

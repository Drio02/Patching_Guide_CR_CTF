<?php
// Patch 1: prepared statement con mysqli
$stmt = $mysqli->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->bind_param("ss", $_POST['username'], $_POST['password']);
$stmt->execute();
$res = $stmt->get_result();

// Patch 2: PDO + cast a entero
$stmt = $pdo->prepare("SELECT * FROM notes WHERE id = ?");
$stmt->execute([(int)$_GET['id']]);
$note = $stmt->fetch();

// Patch 3: PDO con parametros con nombre (sin escapes caseros)
$stmt = $pdo->prepare("SELECT * FROM users WHERE name = :name");
$stmt->execute([':name' => $_GET['name']]);

// Recomendado al crear la conexion PDO:
// $pdo = new PDO($dsn, $u, $p, [
//     PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
//     PDO::ATTR_EMULATE_PREPARES => false,   // prepared statements reales
// ]);

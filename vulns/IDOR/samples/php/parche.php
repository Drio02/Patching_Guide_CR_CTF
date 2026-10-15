<?php
session_start();

// Patch 1: el dueño es parte del WHERE
if (!isset($_SESSION['user_id'])) { http_response_code(401); exit; }
$stmt = $pdo->prepare("SELECT title, body FROM notes WHERE id = ? AND owner_id = ?");
$stmt->execute([(int)$_GET['id'], $_SESSION['user_id']]);
$note = $stmt->fetch();
if (!$note) { http_response_code(404); exit; }
echo json_encode($note);

// Patch 2: la identidad sale de la sesion, se ignora el campo del formulario
$stmt = $pdo->prepare("SELECT * FROM profiles WHERE user_id = ?");
$stmt->execute([$_SESSION['user_id']]);
echo json_encode($stmt->fetch());

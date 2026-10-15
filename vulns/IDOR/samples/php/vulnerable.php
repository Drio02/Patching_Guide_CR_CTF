<?php
session_start();

// Vuln 1: el ID de la nota viene del GET y no se verifica el dueño
if (!isset($_SESSION['user_id'])) { http_response_code(401); exit; }
$stmt = $pdo->prepare("SELECT title, body FROM notes WHERE id = ?");
$stmt->execute([$_GET['id']]);              // ?id=1, ?id=2, ... notas de otros
echo json_encode($stmt->fetch());

// Vuln 2: la identidad viene de un campo oculto del formulario
// <input type="hidden" name="user_id" value="7">
$stmt = $pdo->prepare("SELECT * FROM profiles WHERE user_id = ?");
$stmt->execute([$_POST['user_id']]);
echo json_encode($stmt->fetch());

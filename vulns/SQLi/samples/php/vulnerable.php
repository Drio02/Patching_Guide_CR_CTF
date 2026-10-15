<?php
// Vuln 1: concatenacion directa en el login (mysqli)
$user = $_POST['username'];
$pass = $_POST['password'];
$res = $mysqli->query("SELECT * FROM users WHERE username = '$user' AND password = '$pass'");
// payload: username=admin' -- -

// Vuln 2: id numerico sin comillas (no hace falta cerrar comillas)
$id = $_GET['id'];
$note = $pdo->query("SELECT * FROM notes WHERE id = " . $id)->fetch();
// payload: id=0 UNION SELECT flag, 2, 3 FROM flags

// Vuln 3: "escape" casero insuficiente
$name = str_replace("'", "\\'", $_GET['name']);   // se rompe enviando \' -> \\'
$pdo->query("SELECT * FROM users WHERE name = '$name'");

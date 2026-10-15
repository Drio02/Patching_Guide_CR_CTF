<?php
// MongoDB PHP library
require 'vendor/autoload.php';
$users = (new MongoDB\Client('mongodb://mongo:27017'))->app->users;

// Patch: rechazar arrays y comparar el password en codigo
$username = $_POST['username'] ?? null;
$password = $_POST['password'] ?? null;
if (!is_string($username) || !is_string($password)) { http_response_code(400); exit; }

$user = $users->findOne(['username' => $username]);
if ($user && hash_equals((string)$user['password'], $password)) {
    $_SESSION['user'] = $user['username'];
}

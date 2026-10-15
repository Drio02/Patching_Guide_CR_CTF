<?php
// MongoDB PHP library
require 'vendor/autoload.php';
$users = (new MongoDB\Client('mongodb://mongo:27017'))->app->users;

// Vuln: PHP convierte password[$ne]=x en ['$ne' => 'x']
$user = $users->findOne([
    'username' => $_POST['username'],
    'password' => $_POST['password'],
]);
// POST username=admin&password[$ne]=x
if ($user) { $_SESSION['user'] = $user['username']; }

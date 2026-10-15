<?php
// Twig
require 'vendor/autoload.php';
$twig = new \Twig\Environment(new \Twig\Loader\FilesystemLoader('templates'), ['autoescape' => 'html']);

// Patch: plantilla en archivo, el input como variable
// templates/hello.twig:  Hola {{ name }}
echo $twig->render('hello.twig', ['name' => $_GET['name'] ?? '']);

// Si el usuario debe escribir plantillas: SandboxExtension con politica estricta
// $policy = new \Twig\Sandbox\SecurityPolicy([], [], [], [], []);   // nada permitido
// $twig->addExtension(new \Twig\Extension\SandboxExtension($policy, true));

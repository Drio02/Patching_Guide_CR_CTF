<?php
function e(string $s): string {
    return htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

// Patch 1
echo "<p>Resultados para " . e($_GET['q'] ?? '') . "</p>";

// Patch 2: escapar al mostrar (no al guardar)
foreach ($notes as $n) {
    echo "<div class='note'>" . e($n['body']) . "</div>";
}

// Patch 3: atributo con comillas + escape + solo http/https (bloquea javascript:)
$url = $_GET['url'] ?? '';
if (!preg_match('#^https?://#i', $url)) $url = '#';
echo '<a href="' . e($url) . '">link</a>';

header("Content-Security-Policy: default-src 'self'");

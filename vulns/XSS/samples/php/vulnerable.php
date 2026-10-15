<?php
// Vuln 1: reflejado
echo "<p>Resultados para " . $_GET['q'] . "</p>";

// Vuln 2: almacenado (la nota viene de la base de datos)
foreach ($notes as $n) {
    echo "<div class='note'>" . $n['body'] . "</div>";
}

// Vuln 3: atributo sin comillas
echo "<a href=" . $_GET['url'] . ">link</a>";       // url=x onmouseover=alert(1)

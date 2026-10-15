<?php
// Vuln 1: file_get_contents acepta http://, file://, php://, etc.
echo file_get_contents($_GET['url']);
// url=file:///etc/passwd | http://127.0.0.1/admin.php | php://filter/convert.base64-encode/resource=config.php

// Vuln 2: curl con todos los protocolos y siguiendo redirects
$ch = curl_init($_POST['url']);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
echo curl_exec($ch);                     // gopher://redis:6379/_SET%20...

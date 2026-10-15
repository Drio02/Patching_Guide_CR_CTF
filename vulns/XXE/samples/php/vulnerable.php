<?php
// Vuln: LIBXML_NOENT sustituye las entidades (incluidas las externas)
$xml = file_get_contents('php://input');
$doc = new DOMDocument();
$doc->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD);
echo $doc->getElementsByTagName('body')->item(0)->textContent;

// Mismo problema con SimpleXML:
// $s = simplexml_load_string($xml, 'SimpleXMLElement', LIBXML_NOENT);

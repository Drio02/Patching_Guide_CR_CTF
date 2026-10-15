<?php
$xml = file_get_contents('php://input');

// Patch: sin LIBXML_NOENT ni LIBXML_DTDLOAD, y rechazar documentos con DOCTYPE
if (stripos($xml, '<!DOCTYPE') !== false) { http_response_code(400); exit; }

$doc = new DOMDocument();
$doc->loadXML($xml, LIBXML_NONET);
echo $doc->getElementsByTagName('body')->item(0)->textContent;

// PHP < 8.0: ademas
// libxml_disable_entity_loader(true);

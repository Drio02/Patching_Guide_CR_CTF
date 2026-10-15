const express = require('express');
const fs = require('fs');
const path = require('path');
const router = express.Router();

const BASE = '/srv/notes';

// Vuln 1: path.join normaliza pero NO impide salir de BASE
router.get('/download', (req, res) => {
    const file = path.join(BASE, req.query.file);      // ?file=../../etc/passwd
    res.send(fs.readFileSync(file, 'utf8'));
});

// Vuln 2: sendFile con ruta absoluta construida por concatenacion
router.get('/avatar/:name', (req, res) => {
    res.sendFile(BASE + '/avatars/' + req.params.name);   // ..%2f..%2fetc%2fpasswd
});

// Vuln 3: startsWith sin separador final
router.get('/view', (req, res) => {
    const file = path.resolve(BASE, req.query.file);
    if (!file.startsWith(BASE)) return res.sendStatus(403);   // /srv/notes_backup/... pasa
    res.send(fs.readFileSync(file, 'utf8'));
});

module.exports = router;

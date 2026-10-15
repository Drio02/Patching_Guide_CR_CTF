const express = require('express');
const fs = require('fs');
const path = require('path');
const router = express.Router();

const BASE = fs.realpathSync('/srv/notes');

function safePath(name) {
    const target = path.resolve(BASE, String(name));
    if (!target.startsWith(BASE + path.sep)) return null;
    // realpath resuelve symlinks dentro de BASE que apunten afuera
    let real;
    try { real = fs.realpathSync(target); } catch { return null; }
    return real.startsWith(BASE + path.sep) ? real : null;
}

// Patch 1: resolver + verificar con separador
router.get('/download', (req, res) => {
    const file = safePath(req.query.file);
    if (!file) return res.sendStatus(403);
    res.send(fs.readFileSync(file, 'utf8'));
});

// Patch 2: sendFile con la opcion root rechaza ".." (responde 403)
router.get('/avatar/:name', (req, res) => {
    res.sendFile(req.params.name, { root: path.join(BASE, 'avatars') });
});

// Patch 3: solo nombres simples
router.get('/view', (req, res) => {
    const name = String(req.query.file || '');
    if (!/^[A-Za-z0-9_-]{1,64}$/.test(name)) return res.sendStatus(400);
    res.send(fs.readFileSync(path.join(BASE, name), 'utf8'));
});

module.exports = router;

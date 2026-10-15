const express = require('express');
const net = require('net');
const path = require('path');
const { execFile } = require('child_process');
const router = express.Router();

// Patch 1: execFile no usa shell + validacion de IP + timeout
router.post('/ping', (req, res) => {
    const host = String(req.body.host);
    if (!net.isIP(host)) return res.sendStatus(400);
    execFile('ping', ['-c', '1', host], { timeout: 5000 }, (err, stdout) => {
        res.send(stdout);
    });
});

// Patch 2: argumentos como array + nombre de archivo validado
router.get('/convert', (req, res) => {
    const file = String(req.query.file || '');
    if (!/^[A-Za-z0-9_-]{1,64}\.(png|jpg)$/.test(file)) return res.sendStatus(400);
    execFile('convert', [
        path.join('uploads', file), '-resize', '100x100', path.join('thumbs', file + '.png'),
    ], { timeout: 10000 }, (err) => res.send(err ? 'error' : 'ok'));
});

module.exports = router;

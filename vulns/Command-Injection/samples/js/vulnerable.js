const express = require('express');
const { exec, execSync } = require('child_process');
const router = express.Router();

// Vuln 1: exec usa /bin/sh -c
router.post('/ping', (req, res) => {
    exec('ping -c 1 ' + req.body.host, (err, stdout) => {   // host = "x; cat /data/flags/*"
        res.send(stdout);
    });
});

// Vuln 2: template literal + execSync
router.get('/convert', (req, res) => {
    execSync(`convert uploads/${req.query.file} -resize 100x100 thumbs/${req.query.file}.png`);
    res.send('ok');                                         // file = "a.png;id>public/x"
});

module.exports = router;

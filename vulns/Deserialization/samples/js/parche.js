const express = require('express');
const router = express.Router();

// Patch: JSON.parse solo construye datos (objetos, arrays, strings, numeros)
router.get('/profile', (req, res) => {
    let prefs;
    try {
        prefs = JSON.parse(Buffer.from(String(req.cookies.prefs || ''), 'base64').toString());
    } catch {
        return res.sendStatus(400);
    }
    res.send(`theme: ${String(prefs.theme || 'light')}`);
});

router.post('/settings', (req, res) => {
    try {
        res.json(JSON.parse(req.body.settings));
    } catch {
        res.sendStatus(400);
    }
});

// Cuidado tambien con merges recursivos de objetos del usuario (prototype pollution):
// rechazar claves "__proto__", "constructor", "prototype".

module.exports = router;

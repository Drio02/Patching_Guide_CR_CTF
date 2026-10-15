const express = require('express');
const ejs = require('ejs');
const router = express.Router();

// Patch 1: plantilla fija, el input como dato (<%= %> escapa HTML)
router.get('/hello', (req, res) => {
    res.send(ejs.render('<h1>Hola <%= name %></h1>', { name: String(req.query.name || '') }));
    // o mejor: res.render('hello', { name })  con views/hello.ejs
});

// Patch 2: sin motor de plantillas para contenido del usuario
const escapeHtml = (s) => String(s).replace(/[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

router.post('/card', (req, res) => {
    const out = escapeHtml(req.body.template).replace(/\{user\}/g, escapeHtml(req.session.user));
    res.send(out);
});

module.exports = router;

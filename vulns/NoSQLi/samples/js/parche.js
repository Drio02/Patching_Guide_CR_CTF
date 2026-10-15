const express = require('express');
const bcrypt = require('bcrypt');
const router = express.Router();

// Patch 1: forzar strings y verificar el password fuera de la consulta
router.post('/login', async (req, res) => {
    const { username, password } = req.body;
    if (typeof username !== 'string' || typeof password !== 'string')
        return res.status(400).send('bad request');

    const user = await req.db.collection('users').findOne({ username });
    // Si los passwords estan en texto plano, comparar en codigo; NO cambiar el formato en pleno juego
    const ok = user && (user.passwordHash
        ? await bcrypt.compare(password, user.passwordHash)
        : user.password === password);
    if (!ok) return res.status(401).send('bad credentials');
    req.session.user = user.username;
    res.redirect('/');
});

// Patch 2: String() + el dueño sale de la sesion, no del query
router.get('/notes', async (req, res) => {
    const notes = await req.db.collection('notes')
        .find({ owner: String(req.session.user) }).toArray();
    res.json(notes);
});

// Patch 3: reemplazar $where por un filtro normal
router.get('/search', async (req, res) => {
    const r = await req.db.collection('notes')
        .find({ title: String(req.query.title || ''), owner: req.session.user }).toArray();
    res.json(r);
});

// Alternativa global (si el paquete ya esta instalado):
// app.use(require('express-mongo-sanitize')());

module.exports = router;

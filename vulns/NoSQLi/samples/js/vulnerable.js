const express = require('express');
const router = express.Router();

// Vuln 1: el body JSON llega directo al filtro
router.post('/login', async (req, res) => {
    const user = await req.db.collection('users').findOne({
        username: req.body.username,
        password: req.body.password,          // {"$ne": ""}  -> cualquier password
    });
    if (!user) return res.status(401).send('bad credentials');
    req.session.user = user.username;
    res.redirect('/');
});

// Vuln 2: query string, Express parsea ?owner[$ne]=x como objeto
router.get('/notes', async (req, res) => {
    const notes = await req.db.collection('notes').find({ owner: req.query.owner }).toArray();
    res.json(notes);                          // ?owner[$ne]=nobody -> todas las notas
});

// Vuln 3: $where con concatenacion (JavaScript en el servidor)
router.get('/search', async (req, res) => {
    const r = await req.db.collection('notes')
        .find({ $where: `this.title == '${req.query.title}'` }).toArray();
    res.json(r);                              // title = ' || '1'=='1
});

module.exports = router;

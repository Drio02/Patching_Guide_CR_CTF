const express = require('express');
const router = express.Router();

// Vuln 1: concatenacion en el login
router.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const sql = "SELECT * FROM users WHERE username = '" + username +
                "' AND password = '" + password + "'";
    const [rows] = await req.db.query(sql);   // payload: admin' -- -
    if (rows.length) { req.session.user = rows[0].username; return res.redirect('/'); }
    res.status(401).send('bad credentials');
});

// Vuln 2: template literal en la busqueda
router.get('/notes/search', async (req, res) => {
    const [rows] = await req.db.query(
        `SELECT id, title FROM notes WHERE owner = '${req.session.user}' AND title LIKE '%${req.query.q}%'`
    );  // payload: q=' UNION SELECT id, content FROM notes -- -
    res.json(rows);
});

// Vuln 3: ORDER BY controlado por el usuario
router.get('/notes', async (req, res) => {
    const [rows] = await req.db.query(`SELECT * FROM notes ORDER BY ${req.query.sort}`);
    res.json(rows);
});

module.exports = router;

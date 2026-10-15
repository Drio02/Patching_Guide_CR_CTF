const express = require('express');
const router = express.Router();

// Patch 1: placeholders (mysql2 / sqlite3 usan ?, pg usa $1, $2)
router.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const [rows] = await req.db.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        [String(username), String(password)]     // String(): evita objetos/arrays del body
    );
    if (rows.length) { req.session.user = rows[0].username; return res.redirect('/'); }
    res.status(401).send('bad credentials');
});

// Patch 2: el valor del LIKE va como parametro; los % se agregan fuera del SQL
router.get('/notes/search', async (req, res) => {
    const q = String(req.query.q || '').replace(/[\\%_]/g, '\\$&');
    const [rows] = await req.db.execute(
        'SELECT id, title FROM notes WHERE owner = ? AND title LIKE ?',
        [req.session.user, `%${q}%`]
    );
    res.json(rows);
});

// Patch 3: allowlist para identificadores (no se pueden parametrizar)
const SORTABLE = { title: 'title', date: 'created_at' };
router.get('/notes', async (req, res) => {
    const col = SORTABLE[req.query.sort] || 'created_at';
    const [rows] = await req.db.execute(
        `SELECT * FROM notes WHERE owner = ? ORDER BY ${col}`, [req.session.user]);
    res.json(rows);
});

// Postgres (pg):  await pool.query('SELECT * FROM users WHERE username = $1', [username]);

module.exports = router;

const express = require('express');
const router = express.Router();

// Vuln 1: Number() acepta negativos, "Infinity", "1e309"; parseInt("10abc") = 10
router.post('/buy', async (req, res) => {
    const qty = Number(req.body.qty);                  // -5 -> total negativo -> suma creditos
    const total = qty * PRICES[req.body.item];
    const user = await Users.findById(req.session.userId);
    if (user.credits < total) return res.status(400).send('not enough credits');
    user.credits -= total;
    await user.save();
    res.send(req.body.item === 'flag' ? FLAG : 'ok');
});

// Vuln 2: mass assignment
router.post('/profile', async (req, res) => {
    const user = await Users.findById(req.session.userId);
    Object.assign(user, req.body);                     // {"role": "admin", "credits": 999999}
    await user.save();
    res.send('updated');
});

// Vuln 3: regex con flag g reutilizada -> .test() alterna true/false (lastIndex)
const ID_RE = /^[a-f0-9]{16}$/g;
router.get('/note', (req, res) => {
    if (!ID_RE.test(req.query.id)) return res.sendStatus(400);
    res.json(getNote(req.query.id));
});

// Vuln 4: ?admin=false llega como string "false", que es truthy
router.get('/settings', (req, res) => {
    if (req.query.debug) return res.json(process.env);   // ?debug=0 tambien entra
    res.json({});
});

// Vuln 5: ?tag[]=a llega como array; includes() de array vs string
router.get('/search', (req, res) => {
    if (req.query.tag.includes('<')) return res.sendStatus(400);  // ['<script>'] no incluye '<'
    res.send(`<p>${req.query.tag}</p>`);
});

module.exports = router;

const express = require('express');
const router = express.Router();

// Entero positivo acotado; rechaza "1e3", "-5", "Infinity", "10abc", arrays
function parsePositiveInt(value, max) {
    if (typeof value === 'number') value = String(value);
    if (typeof value !== 'string' || !/^[0-9]{1,9}$/.test(value)) return null;
    const n = Number(value);
    return n > 0 && n <= max ? n : null;
}

// Patch 1: cantidad validada + item en allowlist + descuento atomico
router.post('/buy', async (req, res) => {
    const qty = parsePositiveInt(req.body.qty, 100);
    const price = Object.hasOwn(PRICES, req.body.item) ? PRICES[req.body.item] : null;
    if (qty === null || price === null) return res.sendStatus(400);
    const total = qty * price;
    // solo descuenta si alcanza el saldo, en una sola operacion
    const r = await Users.updateOne(
        { _id: req.session.userId, credits: { $gte: total } },
        { $inc: { credits: -total } });
    if (r.modifiedCount !== 1) return res.status(400).send('not enough credits');
    res.send(req.body.item === 'flag' ? FLAG : 'ok');
});

// Patch 2: copiar solo campos permitidos
const PROFILE_FIELDS = ['displayName', 'bio'];
router.post('/profile', async (req, res) => {
    const update = {};
    for (const f of PROFILE_FIELDS) {
        if (typeof req.body[f] === 'string' && req.body[f].length <= 200) update[f] = req.body[f];
    }
    await Users.updateOne({ _id: req.session.userId }, { $set: update });
    res.send('updated');
});

// Patch 3: sin flag g para validar
const ID_RE = /^[a-f0-9]{16}$/;
router.get('/note', (req, res) => {
    const id = req.query.id;
    if (typeof id !== 'string' || !ID_RE.test(id)) return res.sendStatus(400);
    res.json(getNote(id));
});

// Patch 4: comparar con el valor exacto (y no exponer env en ningun caso)
router.get('/settings', (req, res) => {
    res.json({ debug: req.query.debug === 'true' });
});

// Patch 5: exigir string antes de validar; escapar en la salida
router.get('/search', (req, res) => {
    const tag = req.query.tag;
    if (typeof tag !== 'string' || !/^[\w-]{1,32}$/.test(tag)) return res.sendStatus(400);
    res.send(`<p>${tag}</p>`);
});

module.exports = router;

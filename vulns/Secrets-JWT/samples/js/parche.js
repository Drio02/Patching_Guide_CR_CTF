const express = require('express');
const session = require('express-session');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const fs = require('fs');
const app = express();

// Secreto persistente: env var o archivo en un volumen (mismo valor tras reinicios)
function persistentSecret(envName, file) {
    if (process.env[envName]) return process.env[envName];
    if (!fs.existsSync(file)) fs.writeFileSync(file, crypto.randomBytes(32).toString('hex'));
    return fs.readFileSync(file, 'utf8').trim();
}

// Patch 1
app.use(session({
    secret: persistentSecret('SESSION_SECRET', '/data/session_secret'),
    resave: false,
    saveUninitialized: false,
    cookie: { httpOnly: true, sameSite: 'lax' },
}));

const JWT_SECRET = persistentSecret('JWT_SECRET', '/data/jwt_secret');

function auth(req, res, next) {
    const [scheme, token] = String(req.headers.authorization || '').split(' ');
    if (scheme !== 'Bearer' || !token) return res.sendStatus(401);
    try {
        // Patch 2 y 3: verify + algoritmo fijo
        req.claims = jwt.verify(token, JWT_SECRET, { algorithms: ['HS256'] });
        next();
    } catch {
        res.sendStatus(401);
    }
}

app.get('/api/me', auth, (req, res) => res.json({ user: req.claims.sub }));
app.get('/api/notes', auth, (req, res) => res.json({ user: req.claims.sub }));

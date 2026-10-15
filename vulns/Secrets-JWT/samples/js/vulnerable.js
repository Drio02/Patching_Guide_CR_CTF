const express = require('express');
const session = require('express-session');
const jwt = require('jsonwebtoken');
const app = express();

// Vuln 1: secreto de express-session hardcodeado (el ejemplo de la documentacion)
app.use(session({
    secret: 'keyboard cat',
    resave: false,
    saveUninitialized: true,
}));

const JWT_SECRET = 'secret';

// Vuln 2: jwt.decode NO verifica la firma
app.get('/api/me', (req, res) => {
    const claims = jwt.decode(req.headers.authorization.split(' ')[1]);
    res.json({ user: claims.sub });
});

// Vuln 3: verify sin fijar algorithms (versiones viejas aceptan "none" o confusion RS/HS)
app.get('/api/notes', (req, res) => {
    const claims = jwt.verify(req.headers.authorization.split(' ')[1], JWT_SECRET);
    res.json({ user: claims.sub });
});

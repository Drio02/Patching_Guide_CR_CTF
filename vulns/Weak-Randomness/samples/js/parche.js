const crypto = require('crypto');

// Patch 1
function apiToken() {
    return crypto.randomBytes(16).toString('hex');
}

// Patch 2
function shareId() {
    return crypto.randomUUID();
}

// Patch 3: randomInt evita el sesgo de modulo
function tempPassword(len = 12) {
    const cs = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let p = '';
    for (let i = 0; i < len; i++) p += cs[crypto.randomInt(cs.length)];
    return p;
}

// En el navegador: crypto.getRandomValues(new Uint8Array(16))

module.exports = { apiToken, shareId, tempPassword };

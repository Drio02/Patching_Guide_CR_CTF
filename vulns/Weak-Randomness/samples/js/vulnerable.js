// Vuln 1: token de API con Math.random
function apiToken() {
    return Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2);
}

// Vuln 2: ID de recurso compartible con Date.now como "entropia"
function shareId() {
    return Date.now().toString(16) + Math.floor(Math.random() * 1e6);
}

// Vuln 3: password temporal
function tempPassword(len = 12) {
    const cs = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let p = '';
    for (let i = 0; i < len; i++) p += cs[Math.floor(Math.random() * cs.length)];
    return p;
}

module.exports = { apiToken, shareId, tempPassword };

// ---------- Frontend ----------

// Patch 1: textContent no interpreta HTML
function showLog(xhr) {
    document.getElementById('log').textContent = xhr.responseText;
}

// Patch 2
const name = new URLSearchParams(location.search).get('name') || '';
document.getElementById('greet').textContent = 'Hola ' + name;

// Si de verdad hace falta HTML (ej. markdown renderizado):
// el.innerHTML = DOMPurify.sanitize(html);

// ---------- Backend (Express + EJS) ----------
// views/note.ejs:   <div class="note"><%= note.body %></div>     <%= escapa

// Patch 3: escapar al armar HTML a mano
const escapeHtml = (s) => String(s).replace(/[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
// app.get('/search', (req, res) => res.send('<p>Resultados para ' + escapeHtml(req.query.q) + '</p>'));

// Defensa en profundidad:
// app.use((req, res, next) => { res.set('Content-Security-Policy', "default-src 'self'"); next(); });

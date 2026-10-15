// ---------- Frontend (caso fireworx: src/static/content.js) ----------

// Vuln 1: la respuesta del servidor (con datos del usuario) va a innerHTML
function showLog(xhr) {
    document.getElementById('log').innerHTML = xhr.responseText;
}

// Vuln 2: parametro de la URL al DOM
const name = new URLSearchParams(location.search).get('name');
document.getElementById('greet').innerHTML = 'Hola ' + name;   // ?name=<img src=x onerror=alert(1)>

// ---------- Backend (Express + EJS) ----------
// views/note.ejs:   <div class="note"><%- note.body %></div>     <%- no escapa
// Vuln 3: respuesta HTML armada a mano
// app.get('/search', (req, res) => res.send('<p>Resultados para ' + req.query.q + '</p>'));

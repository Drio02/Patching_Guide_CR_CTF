// Servicio TCP de notas en C (patron tipico de A/D)
// Comandos: LOGIN <user> <pass> | GET <note_id>

#include <stdio.h>
#include <string.h>

struct session {
    int  logged_in;
    char user[32];
};

int  load_note(int id, char *owner, size_t olen, char *body, size_t blen);

// Vuln: solo verifica que haya sesion, no que la nota sea del usuario
void cmd_get(struct session *s, FILE *out, int note_id) {
    char owner[32], body[1024];
    if (!s->logged_in) { fputs("login first\n", out); return; }

    if (load_note(note_id, owner, sizeof owner, body, sizeof body) != 0) {
        fputs("not found\n", out);
        return;
    }
    fprintf(out, "%s\n", body);    // cualquier usuario logueado lee cualquier nota (GET 1, GET 2, ...)
}

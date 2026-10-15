// Servicio TCP de notas en C (patron tipico de A/D)
// Comandos: LOGIN <user> <pass> | GET <note_id>

#include <stdio.h>
#include <string.h>

struct session {
    int  logged_in;
    char user[32];
};

int  load_note(int id, char *owner, size_t olen, char *body, size_t blen);

// Patch: comparar el dueño de la nota con el usuario de la sesion
void cmd_get(struct session *s, FILE *out, int note_id) {
    char owner[32], body[1024];
    if (!s->logged_in) { fputs("login first\n", out); return; }

    // Mismo mensaje para "no existe" y "no es tuya": no se filtra que IDs existen
    if (load_note(note_id, owner, sizeof owner, body, sizeof body) != 0 ||
        strcmp(owner, s->user) != 0) {
        fputs("not found\n", out);
        return;
    }
    fprintf(out, "%s\n", body);
}

// Ojo: strcmp completo, NO strncmp(owner, s->user, strlen(s->user)).
// Con strncmp + strlen del input, un usuario "" o un prefijo ("ali" para "alice") pasaria.

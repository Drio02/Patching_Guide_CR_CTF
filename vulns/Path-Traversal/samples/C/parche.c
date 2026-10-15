#include <ctype.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BASE "/srv/notes"

// Patch 1 (recomendado en A/D): allowlist de caracteres, sin '/' ni '.'
static int valid_name(const char *name) {
    size_t len = strlen(name);
    if (len == 0 || len > 64) return 0;
    for (size_t i = 0; i < len; i++)
        if (!isalnum((unsigned char)name[i]) && name[i] != '_' && name[i] != '-')
            return 0;
    return 1;
}

// Patch 2: realpath + verificacion de prefijo (cubre tambien symlinks)
static int inside_base(const char *path) {
    char resolved[PATH_MAX];
    if (!realpath(path, resolved)) return 0;
    return strncmp(resolved, BASE "/", strlen(BASE "/")) == 0;
}

void send_note(FILE *out, const char *name) {
    char path[256];
    if (!valid_name(name)) { fputs("invalid name\n", out); return; }
    // snprintf limita la escritura; si trunca, se rechaza
    if (snprintf(path, sizeof path, "%s/%s", BASE, name) >= (int)sizeof path) return;
    if (!inside_base(path)) { fputs("forbidden\n", out); return; }

    FILE *f = fopen(path, "r");
    if (!f) { fputs("not found\n", out); return; }
    char buf[512];
    size_t n;
    while ((n = fread(buf, 1, sizeof buf, f)) > 0)
        fwrite(buf, 1, n, out);
    fclose(f);
}

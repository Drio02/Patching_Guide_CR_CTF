#include <stdio.h>
#include <string.h>

#define BASE "/srv/notes"

// Vuln: el nombre de la nota viene del cliente y se concatena sin validar
// Ademas sprintf no tiene limite -> overflow si name es largo
void send_note(FILE *out, const char *name) {
    char path[256];
    sprintf(path, "%s/%s", BASE, name);      // name = "../../etc/passwd"
    FILE *f = fopen(path, "r");
    if (!f) { fputs("not found\n", out); return; }
    char buf[512];
    size_t n;
    while ((n = fread(buf, 1, sizeof buf, f)) > 0)
        fwrite(buf, 1, n, out);
    fclose(f);
}

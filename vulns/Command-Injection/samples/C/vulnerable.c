#include <stdio.h>
#include <stdlib.h>

// Vuln: system() ejecuta "/bin/sh -c <cmd>"
void do_ping(const char *host) {
    char cmd[256];
    snprintf(cmd, sizeof cmd, "ping -c 1 %s", host);   // host = "x;cat /data/flags/*"
    system(cmd);
}

// Vuln: popen() tambien usa la shell
void list_notes(FILE *out, const char *user) {
    char cmd[256], line[256];
    snprintf(cmd, sizeof cmd, "ls notes/%s", user);     // user = "$(id)"
    FILE *p = popen(cmd, "r");
    if (!p) return;
    while (fgets(line, sizeof line, p)) fputs(line, out);
    pclose(p);
}

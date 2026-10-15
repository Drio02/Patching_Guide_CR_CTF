#include <arpa/inet.h>
#include <dirent.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

// Patch 1: validar como IP y ejecutar con fork + execvp (sin shell)
void do_ping(const char *host) {
    struct in_addr a;
    if (inet_pton(AF_INET, host, &a) != 1) return;

    pid_t pid = fork();
    if (pid == 0) {
        char *const argv[] = { "ping", "-c", "1", (char *)host, NULL };
        execvp("ping", argv);
        _exit(127);
    }
    if (pid > 0) waitpid(pid, NULL, 0);
}

// Patch 2: no hace falta un proceso para listar un directorio
static int valid_name(const char *s) {
    if (!*s || strlen(s) > 32) return 0;
    for (; *s; s++)
        if (!isalnum((unsigned char)*s) && *s != '_' && *s != '-') return 0;
    return 1;
}

void list_notes(FILE *out, const char *user) {
    char path[64];
    if (!valid_name(user)) return;
    snprintf(path, sizeof path, "notes/%s", user);
    DIR *d = opendir(path);
    if (!d) return;
    struct dirent *e;
    while ((e = readdir(d)))
        if (e->d_name[0] != '.') fprintf(out, "%s\n", e->d_name);
    closedir(d);
}

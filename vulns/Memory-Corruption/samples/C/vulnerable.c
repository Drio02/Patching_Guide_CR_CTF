#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Estado global: los buffers quedan contiguos en .bss
char hexbuf[64];
int  loggedin = 0;

// Vuln 1 (caso stldoctor): char con signo en %02x
// Un byte >= 0x80 se imprime como "ffffff80" (8 chars). 32 bytes -> hasta 256 chars en hexbuf[64]
// -> overflow hacia loggedin
void hexdump(const char *str, size_t len) {
    char *bp = hexbuf;
    for (size_t i = 0; i < len; i++)
        bp += sprintf(bp, "%02x", str[i]);
}

// Vuln 2: format string
void log_msg(const char *user_msg) {
    printf(user_msg);                // "%p %p %p %s" lee el stack; "%n" escribe
}

// Vuln 3 (caso stldoctor): char vs EOF
// El byte 0xff se lee como -1 == EOF y corta la lectura antes de tiempo
size_t read_name(FILE *f, char *out, size_t max) {
    char c;
    size_t len = 0;
    while ((c = fgetc(f)) != EOF && c && len < max - 1)
        out[len++] = c;
    out[len] = 0;
    return len;
}

// Vuln 4 (caso stldoctor): la longitud sale del input del atacante
int check_password(const char *input, const char *real) {
    return strncmp(input, real, strlen(input)) == 0;   // input "" -> match
}

// Vuln 5: overflow de enteros en el calculo del tamaño
int *alloc_points(size_t n) {
    return malloc(n * sizeof(int) * 3);                 // n grande -> wrap -> buffer chico
}

// Vuln 6: copia sin limite
void set_username(char *dst /* [32] */, const char *src) {
    strcpy(dst, src);
}

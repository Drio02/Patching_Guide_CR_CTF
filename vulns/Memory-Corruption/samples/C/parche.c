#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char hexbuf[64];
int  loggedin = 0;

// Patch 1: cast a unsigned char + snprintf con el espacio restante
void hexdump(const char *str, size_t len) {
    char *bp = hexbuf, *end = hexbuf + sizeof hexbuf;
    for (size_t i = 0; i < len; i++) {
        int w = snprintf(bp, end - bp, "%02x", (unsigned char)str[i]);
        if (w < 0 || w >= end - bp) break;     // no hay espacio: cortar
        bp += w;
    }
}

// Patch 2: el input nunca es el formato
void log_msg(const char *user_msg) {
    printf("%s", user_msg);
}

// Patch 3: int para poder distinguir EOF (-1) del byte 0xff (255)
size_t read_name(FILE *f, char *out, size_t max) {
    int c;
    size_t len = 0;
    while ((c = fgetc(f)) != EOF && c && len < max - 1)
        out[len++] = (char)c;
    out[len] = 0;
    return len;
}

// Patch 4: comparar longitudes completas y en tiempo constante
int check_password(const char *input, const char *real) {
    size_t li = strlen(input), lr = strlen(real);
    if (li != lr || li == 0) return 0;
    unsigned char diff = 0;
    for (size_t i = 0; i < lr; i++) diff |= (unsigned char)(input[i] ^ real[i]);
    return diff == 0;
}

// Patch 5: calloc verifica el overflow de n * size
int *alloc_points(size_t n) {
    if (n > SIZE_MAX / 3) return NULL;
    return calloc(n * 3, sizeof(int));
}

// Patch 6: copia acotada (el tamaño se pasa explicito: sizeof(dst) daria 8 en un puntero)
void set_username(char *dst, size_t dstlen, const char *src) {
    snprintf(dst, dstlen, "%s", src);
}

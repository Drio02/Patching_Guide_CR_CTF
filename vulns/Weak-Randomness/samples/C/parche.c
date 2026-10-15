#include <stdio.h>
#include <stdlib.h>
#include <sys/random.h>     // Linux, glibc >= 2.25

// Patch: getrandom() lee del CSPRNG del kernel
static void secure_bytes(void *buf, size_t n) {
    if (getrandom(buf, n, 0) != (ssize_t)n) abort();
}

void init_rng(void) {
    // Ya no hace falta sembrar nada.
    // Si otras partes del codigo siguen usando rand() para cosas NO sensibles, se puede dejar:
    // unsigned int seed; secure_bytes(&seed, sizeof seed); srand(seed);
}

// Mismo formato (16 hex) para no romper al checker
void new_session_id(char *out, size_t outlen) {
    unsigned int a, b;
    secure_bytes(&a, sizeof a);
    secure_bytes(&b, sizeof b);
    snprintf(out, outlen, "%08x%08x", a, b);
}

// Alternativa portable: leer de /dev/urandom
// FILE *f = fopen("/dev/urandom", "rb"); fread(buf, 1, n, f); fclose(f);

// OJO: si srand(seed) se usa para REGENERAR un keystream que descifra datos guardados,
// cambiarlo rompe los flags viejos. Arreglar la parte explotable y dejar esa derivacion.

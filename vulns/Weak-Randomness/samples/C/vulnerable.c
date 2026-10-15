#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Vuln (caso stldoctor): srand(time(NULL)) al iniciar
// El atacante ejecuta srand(t) para t en [ahora-60, ahora] y obtiene la misma secuencia
void init_rng(void) {
    srand(time(NULL));
}

// ID de sesion / nota predecible
void new_session_id(char *out, size_t outlen) {
    snprintf(out, outlen, "%08x%08x", rand(), rand());
}

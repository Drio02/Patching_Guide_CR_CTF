// Vuln 1
// Clave literal
// ECB manual
// Sin IV ni auth

#include <openssl/aes.h>
#include <string.h>

/* Clave incrustada: recuperable con `strings` o desensamblado */
static const unsigned char KEY[16] = "hardcoded_key_16";

void encrypt_note(const unsigned char *in, unsigned char *out, size_t nblocks) {
    AES_KEY aes;
    AES_set_encrypt_key(KEY, 128, &aes);
    for (size_t i = 0; i < nblocks; i++)
        AES_encrypt(in + i*16, out + i*16, &aes);   /* ECB: bloque igual -> ct igual */
}

// Vuln 2
// memcmp/strcmp sobre secretos
// 

#include <string.h>

static const char *ADMIN_TOKEN = "s3cr3t_admin_token";

int is_admin(const char *supplied) {
    /* memcmp retorna en el primer byte diferente -> fuga temporal */
    return memcmp(supplied, ADMIN_TOKEN, strlen(ADMIN_TOKEN)) == 0;
}
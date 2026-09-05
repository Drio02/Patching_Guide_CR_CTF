// Patch 1
// Clace en el entorno, no en codigo
// AES-GCM, no ECB
// Nonce no reutilizable

#include <openssl/evp.h>
#include <openssl/rand.h>
#include <stdlib.h>

int encrypt_note(const unsigned char *pt, int pt_len,
                 unsigned char *out, int *out_len) {
    unsigned char key[32], nonce[12], tag[16];
    const char *hex = getenv("ENC_KEY");
    if (!hex) return -1;
    for (int i = 0; i < 32; i++) sscanf(hex + 2*i, "%2hhx", &key[i]);
    if (RAND_bytes(nonce, sizeof nonce) != 1) return -1;

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    int len, ok = 0;
    if (EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, key, nonce) == 1 &&
        EVP_EncryptUpdate(ctx, out + 12, &len, pt, pt_len) == 1) {
        int total = len;
        EVP_EncryptFinal_ex(ctx, out + 12 + len, &len);
        total += len;
        EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, 16, tag);
        memcpy(out, nonce, 12);
        memcpy(out + 12 + total, tag, 16);
        *out_len = 12 + total + 16;
        ok = 1;
    }
    EVP_CIPHER_CTX_free(ctx);
    OPENSSL_cleanse(key, sizeof key);              /* borra la clave de memoria */
    return ok ? 0 : -1;
}

// Patch 2

#include <openssl/crypto.h>
#include <string.h>
#include <stdlib.h>

int is_admin(const char *supplied) {
    const char *token = getenv("ADMIN_TOKEN");
    if (!token) return 0;
    size_t n = strlen(token);
    if (strlen(supplied) != n) return 0;
    /* CRYPTO_memcmp NO hace early-exit */
    return CRYPTO_memcmp(supplied, token, n) == 0;
}
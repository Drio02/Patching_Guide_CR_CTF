// Vuln 1
// Clave literal en el codigo
// aes-256-ecb -> ECB byte at a time
// Sin IV ni auth

const crypto = require("crypto");

const KEY = Buffer.from("0123456789abcdef0123456789abcdef"); // 32 bytes hardcodeados

function encryptNote(plaintext) {
  const cipher = crypto.createCipheriv("aes-256-ecb", KEY, null); // ECB
  return Buffer.concat([cipher.update(plaintext), cipher.final()]);
}

// Vuln 2
// Math.random() para tokens, IDs de sesión, OTP, etc.
// Math.random es predecible en V8
// A veces mezclado con Date.now() como "entropía".

function makeToken(len = 32) {
  let t = "";
  const cs = "abcdef0123456789";
  for (let i = 0; i < len; i++)
    t += cs[Math.floor(Math.random() * cs.length)]; // PRNG no seguro
  return t;
}

// Vuln 3
// === / == sobre secretos, tokens o firmas HMAC.
// Diferencias de tiempo según cuántos bytes coinciden.

const API_KEY = "s3cr3t_admin_key";

function isAdmin(supplied) {
  return supplied === API_KEY;   // comparación corto-circuito -> timing
}

// Vuln 4
// jwt.verify sin la opción algorithms
// Secreto corto/adivinable
// algorithm confusion

const jwt = require("jsonwebtoken");

const SECRET = "secret"; // débil + hardcodeado

function verifyToken(token) {
  return jwt.verify(token, SECRET);
}
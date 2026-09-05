// Patch 1
// AES-GCM
// Clave desde entorno, no en codigo

const crypto = require("crypto");

const KEY = Buffer.from(process.env.ENC_KEY, "hex"); // 32 bytes, fuera del código

function encryptNote(plaintext) {
  const iv = crypto.randomBytes(12);                 // nonce único
  const cipher = crypto.createCipheriv("aes-256-gcm", KEY, iv);
  const ct = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([iv, tag, ct]);               // iv || tag || ct
}

// Patch 2
// Utilizar crypto.randomBytes para un mejor PRNG

const crypto = require("crypto");

function makeToken(bytes = 16) {
  return crypto.randomBytes(bytes).toString("hex"); // CSPRNG
}

// Patch 3
// Se utilizan hashes para comparacion y mantenere reliability

const crypto = require("crypto");
const API_KEY = process.env.API_KEY;

function isAdmin(supplied) {
  const a = Buffer.from(supplied || "");
  const b = Buffer.from(API_KEY);
  // timingSafeEqual exige misma longitud -> igualamos con hash previo
  const ha = crypto.createHash("sha256").update(a).digest();
  const hb = crypto.createHash("sha256").update(b).digest();
  return crypto.timingSafeEqual(ha, hb);
}

// Patch 4

const jwt = require("jsonwebtoken");
const SECRET = process.env.JWT_SECRET; // largo y aleatorio, desde entorno

function verifyToken(token) {
  return jwt.verify(token, SECRET, {
    algorithms: ["HS256"],   // fija el algoritmo -> corta none y confusion
    maxAge: "15m",
  });
}
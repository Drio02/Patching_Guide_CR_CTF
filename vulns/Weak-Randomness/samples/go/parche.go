package main

import (
	"crypto/rand"
	"encoding/hex"
	"math/big"
)

// Patch: crypto/rand (lee del CSPRNG del sistema operativo)
func sessionToken() string {
	b := make([]byte, 16)
	if _, err := rand.Read(b); err != nil {
		panic(err)
	}
	return hex.EncodeToString(b)
}

func noteID() int {
	n, err := rand.Int(rand.Reader, big.NewInt(1_000_000))
	if err != nil {
		panic(err)
	}
	return int(n.Int64())
}

// Go 1.24+: rand.Text() devuelve un string aleatorio base32 de 26 caracteres

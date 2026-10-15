package main

import (
	"crypto/rand"
	"encoding/hex"
	"net/http"
	"os"
	"strings"

	"github.com/golang-jwt/jwt/v5"
)

// Patch 1: secreto aleatorio persistido (env var o archivo en un volumen)
var jwtSecret = loadSecret("JWT_SECRET", "/data/jwt_secret")

func loadSecret(env, path string) []byte {
	if v := os.Getenv(env); v != "" {
		return []byte(v)
	}
	if b, err := os.ReadFile(path); err == nil {
		return []byte(strings.TrimSpace(string(b)))
	}
	buf := make([]byte, 32)
	rand.Read(buf)
	s := hex.EncodeToString(buf)
	os.WriteFile(path, []byte(s), 0600)
	return []byte(s)
}

// Patch 2: WithValidMethods fija el algoritmo aceptado
func meHandler(w http.ResponseWriter, r *http.Request) {
	tokenStr := strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer ")
	token, err := jwt.Parse(tokenStr, func(t *jwt.Token) (any, error) {
		return jwtSecret, nil
	}, jwt.WithValidMethods([]string{"HS256"}))
	if err != nil || !token.Valid {
		http.Error(w, "unauthorized", http.StatusUnauthorized)
		return
	}
	sub, _ := token.Claims.GetSubject()
	w.Write([]byte(sub))
}

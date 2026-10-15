package main

import (
	"net/http"
	"strings"

	"github.com/golang-jwt/jwt/v5"
)

// Vuln 1: secreto hardcodeado
var jwtSecret = []byte("secret")

// Vuln 2: el keyfunc no verifica el metodo de firma
func meHandler(w http.ResponseWriter, r *http.Request) {
	tokenStr := strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer ")
	token, err := jwt.Parse(tokenStr, func(t *jwt.Token) (any, error) {
		return jwtSecret, nil
	})
	if err != nil || !token.Valid {
		http.Error(w, "unauthorized", http.StatusUnauthorized)
		return
	}
	sub, _ := token.Claims.GetSubject()
	w.Write([]byte(sub))
}

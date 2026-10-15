package main

import (
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"regexp"
	"strconv"
	"strings"
)

type User struct {
	Username string `json:"username"`
	Password string `json:"password"`
	IsAdmin  bool   `json:"-"` // nunca se lee del JSON
	Credits  int64  `json:"-"`
}

// Patch 1: struct de entrada solo con los campos permitidos + rechazar campos desconocidos
type registerReq struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

var nameRE = regexp.MustCompile(`^[a-z0-9]{3,16}$`) // Patch 3: anclado

func registerHandler(w http.ResponseWriter, r *http.Request) {
	var req registerReq
	dec := json.NewDecoder(http.MaxBytesReader(w, r.Body, 4096))
	dec.DisallowUnknownFields()
	if err := dec.Decode(&req); err != nil || !nameRE.MatchString(req.Username) ||
		len(req.Password) == 0 || len(req.Password) > 128 {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}
	saveUser(User{Username: req.Username, Password: req.Password})
}

// Patch 2: ParseInt con rango explicito
func withdrawHandler(w http.ResponseWriter, r *http.Request) {
	amount, err := strconv.ParseInt(r.FormValue("amount"), 10, 64)
	if err != nil || amount <= 0 || amount > 1_000_000 {
		http.Error(w, "bad amount", http.StatusBadRequest)
		return
	}
	// debitIfEnough: UPDATE ... SET credits = credits - ? WHERE user = ? AND credits >= ?
	if !debitIfEnough(currentUser(r), amount) {
		http.Error(w, "insufficient funds", http.StatusBadRequest)
	}
}

// Patch 4: regex anclada antes de reenviar por un protocolo de lineas
var backend net.Conn

func signupHandler(w http.ResponseWriter, r *http.Request) {
	name := r.FormValue("username")
	if !nameRE.MatchString(name) { // con ^...$ y sin (?m), no puede haber \n, \x00 ni espacios
		http.Error(w, "bad name", http.StatusBadRequest)
		return
	}
	fmt.Fprintf(backend, "REGISTER %s\n", name)
}

// Para campos libres (sin allowlist), rechazar al menos los separadores del protocolo:
func hasControl(s string) bool {
	return strings.ContainsAny(s, "\r\n\x00")
}

// Nota: el paquete regexp de Go usa RE2 (tiempo lineal), asi que es inmune a ReDoS.

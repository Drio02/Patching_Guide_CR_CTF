package main

import (
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"regexp"
	"strconv"
)

type User struct {
	Username string `json:"username"`
	Password string `json:"password"`
	IsAdmin  bool   `json:"is_admin"`
	Credits  int64  `json:"credits"`
}

// Vuln 1: json.Unmarshal sobre el modelo completo -> mass assignment
func registerHandler(w http.ResponseWriter, r *http.Request) {
	var u User
	json.NewDecoder(r.Body).Decode(&u) // {"username":"x","password":"y","is_admin":true,"credits":1e9}
	saveUser(u)
}

// Vuln 2: Atoi acepta negativos
func withdrawHandler(w http.ResponseWriter, r *http.Request) {
	amount, _ := strconv.Atoi(r.FormValue("amount")) // "-500" -> suma saldo
	debit(currentUser(r), int64(amount))
}

// Vuln 3: regex sin anclas busca subcadenas
var nameRE = regexp.MustCompile(`[a-z0-9]{3,16}`)

// Vuln 4: el frontend HTTP reenvia a un backend TCP que habla por lineas
var backend net.Conn

func signupHandler(w http.ResponseWriter, r *http.Request) {
	name := r.FormValue("username") // "eve\nGETFLAG admin" contiene "eve" -> la regex sin anclas pasa
	if !nameRE.MatchString(name) {
		http.Error(w, "bad name", http.StatusBadRequest)
		return
	}
	fmt.Fprintf(backend, "REGISTER %s\n", name) // el backend recibe dos comandos
}

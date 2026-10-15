package main

import (
	"database/sql"
	"fmt"
	"net/http"
)

var db *sql.DB

// Vuln 1: fmt.Sprintf arma la consulta con input del usuario
func loginHandler(w http.ResponseWriter, r *http.Request) {
	user := r.FormValue("username")
	pass := r.FormValue("password")
	q := fmt.Sprintf("SELECT id FROM users WHERE username = '%s' AND password = '%s'", user, pass)
	var id int
	if err := db.QueryRow(q).Scan(&id); err != nil { // payload: admin' --
		http.Error(w, "bad credentials", http.StatusUnauthorized)
		return
	}
	fmt.Fprintf(w, "welcome %d", id)
}

// Vuln 2: concatenacion en la busqueda
func searchHandler(w http.ResponseWriter, r *http.Request) {
	rows, err := db.Query("SELECT title FROM notes WHERE title LIKE '%" + r.URL.Query().Get("q") + "%'")
	if err != nil {
		return
	}
	defer rows.Close()
}

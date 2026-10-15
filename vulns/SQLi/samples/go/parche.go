package main

import (
	"database/sql"
	"fmt"
	"net/http"
	"strings"
)

var db *sql.DB

// Patch 1: placeholders (? para MySQL/SQLite, $1 para Postgres)
func loginHandler(w http.ResponseWriter, r *http.Request) {
	user := r.FormValue("username")
	pass := r.FormValue("password")
	var id int
	err := db.QueryRow("SELECT id FROM users WHERE username = ? AND password = ?", user, pass).Scan(&id)
	if err != nil {
		http.Error(w, "bad credentials", http.StatusUnauthorized)
		return
	}
	fmt.Fprintf(w, "welcome %d", id)
}

// Patch 2: el patron LIKE se arma fuera del SQL y se pasa como parametro
func searchHandler(w http.ResponseWriter, r *http.Request) {
	q := strings.NewReplacer(`\`, `\\`, `%`, `\%`, `_`, `\_`).Replace(r.URL.Query().Get("q"))
	rows, err := db.Query(`SELECT title FROM notes WHERE title LIKE ? ESCAPE '\'`, "%"+q+"%")
	if err != nil {
		http.Error(w, "error", http.StatusInternalServerError)
		return
	}
	defer rows.Close()
}

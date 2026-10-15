package main

import (
	"net/http"
	"os"
	"text/template"
)

type User struct {
	Name     string
	Password string
}

// Metodo exportado: la plantilla del usuario lo puede llamar
func (u User) ReadFile(path string) string {
	b, _ := os.ReadFile(path)
	return string(b)
}

// Vuln: la plantilla viene del usuario; text/template ademas no escapa HTML
func cardHandler(w http.ResponseWriter, r *http.Request) {
	u := User{Name: "alice", Password: "s3cret"}
	tmpl, err := template.New("card").Parse(r.FormValue("template"))
	if err != nil {
		http.Error(w, "bad template", http.StatusBadRequest)
		return
	}
	tmpl.Execute(w, u)
	// template = {{.Password}}  o  {{.ReadFile "/data/flag"}}
}

package main

import (
	"html/template"
	"net/http"
)

type User struct {
	Name     string
	Password string
}

// Patch: plantilla fija (html/template escapa HTML) y solo los datos necesarios
var cardTmpl = template.Must(template.New("card").Parse(`<div>{{.Name}}: {{.Bio}}</div>`))

type cardView struct {
	Name string
	Bio  string
}

func cardHandler(w http.ResponseWriter, r *http.Request) {
	u := User{Name: "alice", Password: "s3cret"}
	// Se pasa una vista sin campos sensibles ni metodos, nunca el struct completo
	cardTmpl.Execute(w, cardView{Name: u.Name, Bio: r.FormValue("bio")})
}

package main

import (
	"fmt"
	"html"
	"html/template"
	"net/http"
)

// Patch 1: html.EscapeString al armar HTML a mano
func searchHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "<p>Resultados para %s</p>", html.EscapeString(r.URL.Query().Get("q")))
}

// Patch 2: html/template escapa segun el contexto (HTML, atributo, JS, URL)
var noteTmpl = template.Must(template.New("n").Parse(`<div class="note">{{.}}</div>`))

func noteHandler(w http.ResponseWriter, r *http.Request) {
	noteTmpl.Execute(w, r.URL.Query().Get("body"))
}

// Patch 3: pasar el string normal, sin convertirlo a template.HTML
var bioTmpl = template.Must(template.New("b").Parse(`<p>{{.}}</p>`))

func bioHandler(w http.ResponseWriter, r *http.Request) {
	bioTmpl.Execute(w, r.URL.Query().Get("bio"))
}

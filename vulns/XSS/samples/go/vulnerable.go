package main

import (
	"fmt"
	"html/template"
	"net/http"
	tt "text/template"
)

// Vuln 1: HTML armado con Fprintf
func searchHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "<p>Resultados para %s</p>", r.URL.Query().Get("q"))
}

// Vuln 2: text/template NO escapa HTML
var noteTmpl = tt.Must(tt.New("n").Parse(`<div class="note">{{.}}</div>`))

func noteHandler(w http.ResponseWriter, r *http.Request) {
	noteTmpl.Execute(w, r.URL.Query().Get("body"))
}

// Vuln 3: template.HTML desactiva el escape de html/template
var bioTmpl = template.Must(template.New("b").Parse(`<p>{{.}}</p>`))

func bioHandler(w http.ResponseWriter, r *http.Request) {
	bioTmpl.Execute(w, template.HTML(r.URL.Query().Get("bio")))
}

package main

import (
	"net/http"
	"os"
	"path/filepath"
)

const baseDir = "/srv/notes"

// Vuln 1: filepath.Join limpia la ruta pero permite salir de baseDir
func downloadHandler(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("file")
	data, err := os.ReadFile(filepath.Join(baseDir, name)) // ?file=../../etc/passwd
	if err != nil {
		http.NotFound(w, r)
		return
	}
	w.Write(data)
}

// Vuln 2: http.ServeFile con un nombre que viene de un parametro (no de r.URL.Path)
func viewHandler(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, baseDir+"/"+r.URL.Query().Get("file"))
}

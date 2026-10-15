package main

import (
	"io"
	"net/http"
	"os"
	"path/filepath"
)

const baseDir = "/srv/notes"

// Patch 1: filepath.IsLocal (Go 1.20+) rechaza "..", rutas absolutas y nombres vacios
func downloadHandler(w http.ResponseWriter, r *http.Request) {
	name := r.URL.Query().Get("file")
	if !filepath.IsLocal(name) {
		http.Error(w, "forbidden", http.StatusForbidden)
		return
	}
	data, err := os.ReadFile(filepath.Join(baseDir, name))
	if err != nil {
		http.NotFound(w, r)
		return
	}
	w.Write(data)
}

// Patch 2: os.Root (Go 1.24+) confina TODAS las operaciones al directorio, incluidos symlinks
var root, _ = os.OpenRoot(baseDir)

func viewHandler(w http.ResponseWriter, r *http.Request) {
	f, err := root.Open(r.URL.Query().Get("file"))
	if err != nil {
		http.Error(w, "forbidden", http.StatusForbidden)
		return
	}
	defer f.Close()
	io.Copy(w, f)
}

// Alternativa para Go < 1.20:
//   full := filepath.Join(baseDir, filepath.Clean("/"+name))   // el "/" inicial ancla la ruta
//   if !strings.HasPrefix(full, baseDir+string(os.PathSeparator)) { 403 }

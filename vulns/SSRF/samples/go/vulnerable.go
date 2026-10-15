package main

import (
	"io"
	"net/http"
)

// Vuln: http.Get con la URL del usuario (sigue hasta 10 redirects por defecto)
func fetchHandler(w http.ResponseWriter, r *http.Request) {
	resp, err := http.Get(r.FormValue("url")) // http://127.0.0.1:8080/admin
	if err != nil {
		http.Error(w, "error", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()
	io.Copy(w, resp.Body)
}

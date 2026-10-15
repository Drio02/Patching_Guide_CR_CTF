package main

import (
	"context"
	"net"
	"net/http"
	"os/exec"
	"strings"
	"time"
)

// Patch 1: argumentos separados (sin shell) + IP validada + timeout con contexto
func pingHandler(w http.ResponseWriter, r *http.Request) {
	ip := net.ParseIP(r.FormValue("host"))
	if ip == nil {
		http.Error(w, "bad host", http.StatusBadRequest)
		return
	}
	ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
	defer cancel()
	out, _ := exec.CommandContext(ctx, "ping", "-c", "1", ip.String()).CombinedOutput()
	w.Write(out)
}

// Patch 2: rechazar opciones y separar con "--"
func cloneHandler(w http.ResponseWriter, r *http.Request) {
	repo := r.FormValue("repo")
	if strings.HasPrefix(repo, "-") || !strings.HasPrefix(repo, "https://") {
		http.Error(w, "bad repo", http.StatusBadRequest)
		return
	}
	out, _ := exec.Command("git", "ls-remote", "--", repo).CombinedOutput()
	w.Write(out)
}

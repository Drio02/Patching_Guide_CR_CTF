package main

import (
	"net/http"
	"os/exec"
)

// Vuln: exec.Command no usa shell... salvo que se invoque "sh -c"
func pingHandler(w http.ResponseWriter, r *http.Request) {
	host := r.FormValue("host")
	out, _ := exec.Command("sh", "-c", "ping -c 1 "+host).CombinedOutput() // host = "x; cat /flags/*"
	w.Write(out)
}

// Vuln: sin shell, pero el usuario controla una opcion de git
func cloneHandler(w http.ResponseWriter, r *http.Request) {
	repo := r.FormValue("repo") // repo = "--upload-pack=touch /tmp/pwned"
	out, _ := exec.Command("git", "ls-remote", repo).CombinedOutput()
	w.Write(out)
}

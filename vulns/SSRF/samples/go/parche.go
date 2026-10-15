package main

import (
	"errors"
	"io"
	"net"
	"net/http"
	"net/url"
	"syscall"
	"time"
)

// Patch: la verificacion ocurre en el Dialer, sobre la IP a la que REALMENTE se conecta.
// Asi se cubren redirects y DNS rebinding sin logica extra.
var safeClient = &http.Client{
	Timeout: 5 * time.Second,
	CheckRedirect: func(req *http.Request, via []*http.Request) error {
		return http.ErrUseLastResponse // no seguir redirects
	},
	Transport: &http.Transport{
		DialContext: (&net.Dialer{
			Timeout: 3 * time.Second,
			Control: func(network, address string, c syscall.RawConn) error {
				host, _, err := net.SplitHostPort(address)
				if err != nil {
					return err
				}
				ip := net.ParseIP(host)
				if ip == nil || ip.IsLoopback() || ip.IsPrivate() || ip.IsLinkLocalUnicast() ||
					ip.IsLinkLocalMulticast() || ip.IsUnspecified() || ip.IsMulticast() {
					return errors.New("destino interno bloqueado")
				}
				return nil
			},
		}).DialContext,
	},
}

func fetchHandler(w http.ResponseWriter, r *http.Request) {
	u, err := url.Parse(r.FormValue("url"))
	if err != nil || (u.Scheme != "http" && u.Scheme != "https") {
		http.Error(w, "bad url", http.StatusBadRequest)
		return
	}
	resp, err := safeClient.Get(u.String())
	if err != nil {
		http.Error(w, "forbidden", http.StatusForbidden)
		return
	}
	defer resp.Body.Close()
	io.Copy(w, io.LimitReader(resp.Body, 1<<20))
}

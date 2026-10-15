package main

import (
	"fmt"
	"math/rand"
	"time"
)

// Vuln: math/rand es determinista; con semilla de la hora es trivial de predecir
func init() {
	rand.Seed(time.Now().Unix())
}

func sessionToken() string {
	return fmt.Sprintf("%016x%016x", rand.Uint64(), rand.Uint64())
}

func noteID() int {
	return rand.Intn(1_000_000)
}

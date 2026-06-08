package main

import (
    "encoding/json"
    "errors"
    "net/http"
    "strconv"

    "github.com/gorilla/mux"
)

type contextKey string

const userIDKey contextKey = "userID"

func getOrderHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
    orderID, err := strconv.Atoi(vars["orderID"])
    if err != nil {
        http.Error(w, "invalid id", http.StatusBadRequest)
        return
    }

    // La identidad del usuario se obtiene del contexto
    userID, ok := r.Context().Value(userIDKey).(int)
    if !ok {
        http.Error(w, "unauthorized", http.StatusUnauthorized)
        return
    }

	// Autorización aplicada como filtro en la query: si la orden no
    // pertenece al usuario, la consulta no devuelve resultado.
    order, err := db.GetOrderByIDAndUser(orderID, userID)
    if err != nil {
        http.Error(w, "order not found", http.StatusNotFound)
        return
    }

    json.NewEncoder(w).Encode(order)
}

// La consulta para el GetOrder lleva verificacion dentro de sus propios datos
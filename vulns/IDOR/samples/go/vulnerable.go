package main

import (
    "encoding/json"
    "net/http"
    "strconv"

    "github.com/gorilla/mux"
)

type Order struct {
    ID       int     `json:"id"`
    UserID   int     `json:"user_id"`
    Total    float64 `json:"total"`
    Shipping string  `json:"shipping_address"`
}

func getOrderHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
    orderID, err := strconv.Atoi(vars["orderID"])
    if err != nil {
        http.Error(w, "invalid id", http.StatusBadRequest)
        return
    }

	// IDOR: se recupera la orden unicamente por su ID.
	// No se contrasta con el ID del usuario autenticado

	    order, err := db.GetOrderByID(orderID)
    if err != nil {
        http.Error(w, "order not found", http.StatusNotFound)
        return
    }

    json.NewEncoder(w).Encode(order)
}

// Se confirma autenticacion, pero ignora la identidad. Un usuario puede iterar y leer pedidos ajenos.

//-----------------------------------------------------------------------------------------------------
package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"

	"github.com/err/exampleApi/docs"
	"github.com/gorilla/mux"
)

func main() {
	docs.SwaggerInfo.Title = "Example API"
	r := mux.NewRouter()
	r.HandleFunc("/health", handler)
	r.HandleFunc("/balance", balanceHandler)
	r.HandleFunc("/articles", handler)

	srv := &http.Server{
		Handler: r,
		Addr:    "0.0.0.0:8000",
		// Good practice: enforce timeouts for servers you create!
		WriteTimeout: 15 * time.Second,
		ReadTimeout:  15 * time.Second,
	}
	println("Server started at port 8000")
	log.Fatal(srv.ListenAndServe())
}

// @Summary Transfers money between two user ids
// @Description This endpoint transfers money between two user ids
// @Produce  json
// @Success 200
// @Param fromUserId query string false "From user Id"
// @Param toUserId query string false "To user Id"
// @Param amount query string false "Amount to transfer"
// @Router /transfer [post]
func handler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Gorilla!\n"))
}

type BalanceResponse struct {
	Balance string `json:"balance"`
	UserId  string `json:"userId"`
}

// @Summary Gets the balance of a user given an user id
// @Description Gets the balance of a user given an user id
// @Produce  json
// @Success 200
// @Param userId query string true "User id is the unique identitier of the user"
// @Router /balance [post]
func balanceHandler(w http.ResponseWriter, r *http.Request) {
	userId := r.URL.Query().Get("userId")
	balance := "100"
	jsonResponse, err := json.Marshal(BalanceResponse{Balance: balance, UserId: userId})
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(jsonResponse)
}

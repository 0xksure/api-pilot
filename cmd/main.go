package main

import (
	"net/http"

	"github.com/err/exampleApi/docs"
	"github.com/gorilla/mux"
)

func main() {
	docs.SwaggerInfo.Title = "Example API"
	r := mux.NewRouter()
	r.HandleFunc("/", handler)
	r.HandleFunc("/balance", balanceHandler)
	r.HandleFunc("/articles", handler)
	http.Handle("/", r)
}

// @Summary Ping
// @Description check connection
// @Produce  json
// @Success 200
// @Param name query string false "Account Id"
// @Router /ping [get]
func handler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Gorilla!\n"))
}

// @Summary Gets the balance of a user given an user id
// @Description Gets the balance of a user given an user id
// @Produce  json
// @Success 200
// @Param userId query string true "User id is the unique identitier of the user"
// @Router /balance [get]
func balanceHandler(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Gorilla!\n"))
}

package main

import (
    "log"
    "net/http"
)

func main() {

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        http.ServeFile(w, r, "sudoku.html")
    })

    log.Fatal(http.ListenAndServe(":8000", nil))

}

package main

import (
  "fmt"
  "html/template"
  "io"
  "os"
  "log"
  "net/http"
  "os/exec"
)

func main() {

  http.HandleFunc("/sudoku.html", func(w http.ResponseWriter, r *http.Request) {

    query := r.URL.Query()
    vorgabenListe := query["sudoku_vorgaben"]
    if len(vorgabenListe) == 0 {
      http.ServeFile(w, r, "sudoku.html")
      return
    }

    sudokuVorgabe := vorgabenListe[0]
    fmt.Printf("Sudoku Vorgabe ist %s\n", sudokuVorgabe)

    command := exec.Command("python3", "sudoku.py")

    stdin, err := command.StdinPipe()
    if err != nil {
      fmt.Println(err)
      return
    }

    stdin.Write([]byte(sudokuVorgabe))
    stdin.Close()

    stderr, err := command.StderrPipe()
    if err != nil {
      fmt.Println(err)
    }

    stdout, err := command.StdoutPipe()
    if err != nil {
      fmt.Println(err)
    }

    if err := command.Start(); err != nil {
      fmt.Println(err)
    }

    slurp, _ := io.ReadAll(stderr)
    fmt.Printf("%s", slurp)

    endzustand, _ := io.ReadAll(stdout)
    fmt.Printf("%s", endzustand)

    if err := command.Wait(); err != nil {
      fmt.Println(err)
    }

    // Write a representation final state into the HTML file
    // before the HTML file sending to the browser.
    htmlFile, err := template.ParseFiles("sudoku.html")
    if err != nil {
        fmt.Println(err)
    }
    err = htmlFile.Execute(w, string(endzustand))
    if err != nil {
        fmt.Println(err)
    }
  })

  http.HandleFunc("/sat.html", func(w http.ResponseWriter, r *http.Request) {

    query := r.URL.Query()
    programmListe := query["sudoku_vorgaben"]
    if len(programmListe) == 0 {

      htmlFile, err := template.ParseFiles("sat.html")
      if err != nil {
        fmt.Println(err)
      }
      err = htmlFile.Execute(w, "")
      if err != nil {
        fmt.Println(err)
      }
      return
    }

    satProgramm := programmListe[0]
    fmt.Printf("Das eingegebene SAT Programm ist %s\n", satProgramm)

    f, err := os.Create("sat_programm.mod")
    if err != nil {
        fmt.Println(err)
        return
    }
    l, err := f.WriteString(satProgramm)
    if err != nil {
        fmt.Println(err)
        f.Close()
        return
    }
    fmt.Println(l, "bytes written successfully into sat_programm.mod")
    err = f.Close()
    if err != nil {
        fmt.Println(err)
        return
    }

    // Kompiliere eine .mod Datei mit allgemeinem Problem
    // in eine .cpo Datei mit konkretem Problem.
    command := exec.Command(
      "/opt/ibm/ILOG/CPLEX_Studio_Community201/opl/bin/x86-64_linux/oplrun",
      "-v",
      "sat_programm.mod")

    stderr, err := command.StderrPipe()
    if err != nil {
      fmt.Println(err)
    }

    stdout, err := command.StdoutPipe()
    if err != nil {
      fmt.Println(err)
    }

    if err := command.Start(); err != nil {
      fmt.Println(err)
    }

    slurp, _ := io.ReadAll(stderr)
    fmt.Printf("%s", slurp)

    endzustand, _ := io.ReadAll(stdout)
    fmt.Printf("%s", endzustand)

    if err := command.Wait(); err != nil {
      fmt.Println(err)
    }

    htmlFile, err := template.ParseFiles("sat.html")
    if err != nil {
        fmt.Println(err)
    }
    err = htmlFile.Execute(w, string(endzustand))
    if err != nil {
        fmt.Println(err)
    }
  })

  log.Fatal(http.ListenAndServe(":80", nil))
}

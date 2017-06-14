package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"github.com/gorilla/mux"
)

type Release struct {
	ReleaseId string `json:"releaseId"`
	Url       string `json:"url"`
}

type Regress struct {
	SetId   string `json:"setid"`
	Message string `json:"message"`
	Url     string `json:"url"`
}

func main() {
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/ispw/ispw/releases/", CreateRelease).Methods("POST")
	//router.HandleFunc("/ispw/ispw/releases/{release_id}", GetReleaseInformation).Methods("GET")
	//router.HandleFunc("/ispw/ispw/releases/{release_id}/tasks/promote?level={level}", Promote).Methods("POST")
	//router.HandleFunc("/ispw/ispw/releases/{release_id}/tasks/deploy?level={level}", Deploy).Methods("POST")
	//router.HandleFunc("/ispw/ispw/sets/%s", GetSetInformation).Methods("GET")
	router.HandleFunc("/ispw/ispw/releases/{release_id}/tasks/regress?level={level}", Regress).Methods("POST")

	log.Fatal(http.ListenAndServe(":8080", router))
}

// CreateRelease sends a dummy response back
func CreateRelease(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")
	c := Release{"relid", "http://ispw:8080/ispw/ispw/releases/relid"}
	outgoingJSON, err := json.Marshal(c)
	if err != nil {
		log.Println(err.Error())
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	res.WriteHeader(http.StatusCreated)
	fmt.Fprint(res, string(outgoingJSON))
}

// Regress sends a dummy response back
func Regress(res http.ResponseWriter, req *http.Request) {
	res.Header().Set("Content-Type", "application/json")
	c := Regress{"ISPW2345", "This worked", "http://foobarsoft.com/ispw/w3t/sets/s0123456"}
	outgoingJSON, err := json.Marshal(c)
	if err != nil {
		log.Println(err.Error())
		http.Error(res, err.Error(), http.StatusInternalServerError)
		return
	}
	res.WriteHeader(http.StatusCreated)
	fmt.Fprint(res, string(outgoingJSON))

}

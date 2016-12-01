package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"github.com/gorilla/mux"
)

type Release struct {
	ReleaseId  string `json:"releaseId"`
	Url string `json:"url"`
}

func main() {
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/ispw/ispw/releases/", CreateRelease).Methods("POST")
	//router.HandleFunc("/ispw/ispw/releases/{release_id}", GetReleaseInformation).Methods("GET")
	//router.HandleFunc("/ispw/ispw/releases/{release_id}/tasks/promote?level={level}", Promote).Methods("POST")
	//router.HandleFunc("/ispw/ispw/releases/{release_id}/tasks/deploy?level={level}", Deploy).Methods("POST")
	//router.HandleFunc("/ispw/ispw/sets/%s", GetSetInformation).Methods("GET")

	log.Fatal(http.ListenAndServe(":8080", router))
}

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

FROM golang:latest
RUN mkdir /app
ADD src/test/resources/docker/ispw/. /app/
WORKDIR /app

# Install the Gorilla package
RUN go get github.com/gorilla/mux

RUN go build -o main .
CMD ["/app/main"]

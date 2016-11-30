FROM golang:latest
RUN mkdir /app
ADD . /app/
WORKDIR /app

# Install the Martini package
RUN go get github.com/go-martini/martini

RUN go build -o main .
CMD ["/app/main"]

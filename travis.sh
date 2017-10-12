#!/usr/bin/env bash
set -ev

docker run --rm -d -p 28080:8080 --name ispw xebialabs/xl-docker-demo-ispw:latest
./gradlew compileDocker
docker stop ispw


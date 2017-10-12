#!/usr/bin/env bash
set -ev

docker run -d -p 28080:8080 xebialabs/xl-docker-demo-ispw:releases
./gradlew compileDocker


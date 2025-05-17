FROM alpine:latest

RUN apk update && apk add --no-cache \
    bash \
    curl \
    grep \
    coreutils \
    wget

WORKDIR /workspace
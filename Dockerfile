FROM ubuntu:latest
LABEL authors="askou"

ENTRYPOINT ["top", "-b"]
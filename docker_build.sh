#!/usr/bin/env bash

docker build -t stemmers:latest-alpine \
             -t stemmers:0.0.14-alpine \
             .

docker build -f pypy.Dockerfile \
             -t stemmers:latest-pypy \
             -t stemmers:0.0.14-pypy \
             .

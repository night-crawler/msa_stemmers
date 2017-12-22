#!/usr/bin/env bash

docker build -t docker.force.fm/msa/stemmers:latest \
             -t docker.force.fm/msa/stemmers:0.0.12 \
             .

#!/usr/bin/env bash

docker build -t docker.force.fm/msa/msa_stemmers:latest \
             -t docker.force.fm/msa/msa_stemmers:0.0.10 \
             -t ncrawler/msa_stemmers:latest \
             -t ncrawler/msa_stemmers:0.0.11 \
             .

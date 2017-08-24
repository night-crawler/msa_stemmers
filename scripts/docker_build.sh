#!/usr/bin/env bash

docker build -t docker.force.fm/ncrawler/msa_stemmers:latest \
             -t docker.force.fm/ncrawler/msa_stemmers:0.0.7 \
             -t ncrawler/msa_stemmers:latest \
             -t ncrawler/msa_stemmers:0.0.7 \
             .

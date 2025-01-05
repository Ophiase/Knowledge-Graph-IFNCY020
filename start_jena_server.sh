#!/bin/bash

# Variables
JENA_VERSION="5.2.0"
JENA_URL="https://downloads.apache.org/jena/binaries/apache-jena-${JENA_VERSION}.tar.gz"
FUSEKI_URL="https://downloads.apache.org/jena/binaries/apache-jena-fuseki-${JENA_VERSION}.tar.gz"

JENA_DIR="apache-jena-${JENA_VERSION}"
FUSEKI_DIR="apache-jena-fuseki-${JENA_VERSION}"

if [ -d "$FUSEKI_DIR" ]; then
    echo "Starting Fuseki server..."
    "${FUSEKI_DIR}/fuseki-server" --update --mem /ds &
    echo "Fuseki server started at http://localhost:3030"
else
    echo "Fuseki server directory not found. Please run 'make setup_server' first."
fi

#!/bin/bash

# Variables
JENA_VERSION="5.2.0"
JENA_URL="https://downloads.apache.org/jena/binaries/apache-jena-${JENA_VERSION}.tar.gz"
FUSEKI_URL="https://downloads.apache.org/jena/binaries/apache-jena-fuseki-${JENA_VERSION}.tar.gz"

JENA_DIR="apache-jena-${JENA_VERSION}"
FUSEKI_DIR="apache-jena-fuseki-${JENA_VERSION}"

# Download and extract Apache Jena if not already present
if [ ! -d "$JENA_DIR" ]; then
    echo "Downloading Apache Jena..."
    wget -q "$JENA_URL" -O "apache-jena-${JENA_VERSION}.tar.gz"

    echo "Extracting Apache Jena..."
    tar -xzf "apache-jena-${JENA_VERSION}.tar.gz"
    rm -f "apache-jena-${JENA_VERSION}.tar.gz"
fi

# Download and extract Apache Jena Fuseki if not already present
if [ ! -d "$FUSEKI_DIR" ]; then
    echo "Downloading Apache Jena Fuseki..."
    wget -q "$FUSEKI_URL" -O "apache-jena-fuseki-${JENA_VERSION}.tar.gz"

    echo "Extracting Apache Jena Fuseki..."
    tar -xzf "apache-jena-fuseki-${JENA_VERSION}.tar.gz"
    rm -f "apache-jena-fuseki-${JENA_VERSION}.tar.gz"
fi

echo "Apache Jena and Fuseki server setup complete."

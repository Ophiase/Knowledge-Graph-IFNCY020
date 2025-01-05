#!/bin/bash

FUSEKI_URL="http://localhost:3030"
DATASET="ds"
RDF_FILE="data/geonames.rdf"

# Check if Fuseki server is running
if curl -s --head  --request GET $FUSEKI_URL | grep "200 OK" > /dev/null; then 
    echo "Fuseki server is running..."
else
    echo "Fuseki server is not running. Please start the server first."
    exit 1
fi

# Load RDF data into the dataset
echo "Loading RDF data into the dataset..."
curl -X POST --data-binary @"$RDF_FILE" \
     --header "Content-Type: application/rdf+xml" \
     "$FUSEKI_URL/$DATASET/data?default"
echo "RDF data loaded successfully."

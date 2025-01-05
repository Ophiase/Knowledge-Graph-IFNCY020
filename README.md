# Knowledge-Graph-IFNCY020

🏗️ Work In Progress | Deadline: 5 Jan. 2025

## Summary

- [Installation](#installation)
  - [Setup a server](#setup-a-server)
- [Usage](#usage)
  - [Run Basic Queries](#run-basic-queries)
  - [Ontology](#ontology)
- [Documentation](#documentation)
  - [Data](#data)
    - [Geonames](#geonames)
    - [Wikidata](#wikidata)
    - [DBpedia](#dbpedia)
    - [Open-Drug](#open-drug)
    - [PubMed](#pubmed)
  - [Data Loading and Transformation](#data-loading-and-transformation)
  - [Ontology](#ontology)
  - [TODO](#todo)

## Installation

```bash
# download, transform, merge
make download 
make transform
make merge
```

### Setup a server

Requires: Apache Jena, Riot, Fuseki

```bash
# for script requiring org.apache.jena,
# do not forget to add JENA to java class path in .zshrc or .bashrc
export CLASSPATH=$CLASSPATH:$JENAROOT/lib/*
```

## Usage

### Run Basic Queries

```bash
make basic_queries
```

### Ontology

```bash
python3 reasoning.py
```

## Documentation

### Data

#### 🔵 Geonames
Geonames provides geographical data such as cities, administrative divisions, and time zones. The data is downloaded as tab-delimited text files, transformed into RDF format using `transform_geonames.py`, and integrated into the knowledge graph. The transformation includes mapping columns to RDF properties and creating triples for each entity. For example:
- **Cities**: `<City> <name> <asciiname> <latitude> <longitude> <population> <country_code> <timezone>`
- **Country Info**: `<Country> <ISO> <ISO3> <Country> <Capital> <Population> <Continent> <CurrencyCode>`

#### 🔴 Wikidata *(Sparql)*
Wikidata offers structured data about various entities. We fetch data about cities and countries, including labels and relationships, using SPARQL queries in `download_sparql.py`. The data is saved into RDF format and includes properties such as population, area, and coordinates. The transformation involves converting JSON results from SPARQL queries into RDF triples. For example:
- **Cities**: `<City> <name> <country> <population> <area> <latitude> <longitude>`
- **Countries**: `<Country> <name> <population> <area> <capital>`

#### 🔴 DBpedia *(Sparql)*
DBpedia extracts structured information from Wikipedia. We fetch data about cities and countries, including labels and relationships, using SPARQL queries in `download_sparql.py`. The data is saved into RDF format and includes properties such as population, area, and coordinates. The transformation involves converting JSON results from SPARQL queries into RDF triples. For example:
- **Cities**: `<City> <name> <country> <population> <area> <latitude> <longitude>`
- **Countries**: `<Country> <name> <population> <area> <capital>`

#### 🟢 Open-Drug *(Kaggle)*
Open-Drug provides data about drugs, conditions, interactions, and manufacturers. The data is downloaded from Kaggle, transformed into RDF format using `transform_open_drug.py`, and integrated into the knowledge graph. The transformation includes mapping columns to RDF properties and creating triples for each entity. For example:
- **Drugs**: `<Drug> <name> <wiki_url> <drugbank_url>`
- **Conditions**: `<Condition> <name> <source_id> <url>`
- **Interactions**: `<Interaction> <source_drug_id> <target_drug_id>`
- **Manufacturers**: `<Manufacturer> <name>`

#### 🟢 PubMed *(Kaggle)*
PubMed provides a large dataset of biomedical literature. Due to its size (50GB), it is not included in this project.

### Data Loading and Transformation

1. **Download**: Data is downloaded from various sources using `download_kaggle.py`, `download_geonames.py`, and `download_sparql.py`.
2. **Transform**: Data is transformed into RDF format using `transform_open_drug.py` and `transform_geonames.py`. 
    - The transformation scripts map columns to RDF properties and create triples for each entity.
3. **Merge**: All RDF files are merged into a single RDF file using `merge_rdf.py`.

### Ontology

The ontology defines the structure of the knowledge graph, including classes, properties, and relationships. It ensures consistency and enables reasoning over the data. The ontology is defined in `ontology.ttl` and includes classes such as City, Country, and Drug, and properties such as locatedIn, population, and name.

### TODO

- **Wikidata and DBpedia**: Enhance the data fetching to include more properties such as population, area, and coordinates.
- **Reasoning**: Apply more advanced reasoning techniques to infer new knowledge from the data.
- **Queries**: Develop more complex SPARQL queries to demonstrate the integration of different datasets.
- **Refactoring**: Convert everything to camelcase.
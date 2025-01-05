# Knowledge-Graph-IFNCY020

🏗️ Work In Progress | Deadline: 5 Jan. 2025

## Installation

```python
# download, transform, merge
make download 
make transform
make merge
```

### Setup a server

Requires : Apache Jena, Riot, Fuseki

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

#### Geonames
#### Wikidata
#### Dbpedia
#### Open-Drug
#### PubMed

We ignore this one (too heavy to process, 50G to download)
# [Knowledge Graph IFNCY020](https://github.com/Ophiase/Knowledge-Graph-IFNCY020)

🏗️ Work In Progress | Deadline: 5 Jan. 2025

This project involves creating a basic knowledge graph for a university assignment. The knowledge graph integrates data from various sources, including Geonames, Wikidata, DBpedia, Open-Drug, and PubMed. The data is downloaded, transformed into RDF format, and merged into a single RDF file. The ontology defines the structure of the knowledge graph, ensuring consistency and enabling reasoning over the data. The project includes scripts for data downloading, transformation, and merging, as well as examples of basic queries and reasoning.

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
  - [Challenges](#challenges)
  - [Conclusion](#conclusion)
  - [Resources](#resources)
  - [TODO](#todo)

## Installation

```bash
# pip dependancies
make pip 

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

```bash
# todo, setup the server
```

## Usage

### Run Basic Queries

```bash
make basic_queries
```

### Ontology

```bash
make reasoning
```

## Documentation

### Data

#### 🔵 Geonames
Geonames provides geographical data such as cities, administrative divisions, and time zones. The data is downloaded with [download_geonames.py](./download_geonames.py) as tab-delimited text files, transformed into RDF format using [transform_geonames.py](./transform_geonames.py), and integrated into the knowledge graph. The transformation includes mapping columns to RDF properties and creating triples for each entity. For example:
- **city**: `<city> <name> <ascii_name> <latitude> <longitude> <population> <country_code> <timezone>`
- **country_info**: `<country> <iso> <iso3> <country> <capital> <population> <Continent> <currency_code>`

#### 🔴 Wikidata *(Sparql)*
Wikidata offers structured data about various entities. We fetch data about cities and countries, including labels and relationships, using SPARQL queries in [download_sparql.py](./download_sparql.py). The data is saved into RDF format and includes properties such as population, area, and coordinates. The transformation involves converting JSON results from SPARQL queries into RDF triples. For example:
- **cities**: `<city> <name> <country> <population> <area> <latitude> <longitude>`
- **countries**: `<country> <name> <population> <area> <capital>`

#### 🔴 DBpedia *(Sparql)*
DBpedia extracts structured information from Wikipedia. We fetch data about cities and countries, including labels and relationships, using SPARQL queries in [download_sparql.py](./download_sparql.py). The data is saved into RDF format and includes properties such as population, area, and coordinates. The transformation involves converting JSON results from SPARQL queries into RDF triples. For example:
- **cities**: `<city> <name> <country> <population> <area> <latitude> <longitude>`
- **countries**: `<country> <name> <population> <area> <capital>`

#### 🟢 [Open-Drug](https://www.kaggle.com/datasets/mannbrinson/open-drug-knowledge-graph) *(Kaggle)*
Open-Drug provides data about drugs, conditions, interactions, and manufacturers. The data is downloaded from Kaggle with [download_kaggle.py](./download_kaggle.py), transformed into RDF format using [transform_open_drug.py](./transform_open_drug.py), and integrated into the knowledge graph. The transformation includes mapping columns to RDF properties and creating triples for each entity. For example:
- **drugs**: `<drug> <name> <wiki_url> <drugbank_url>`
- **conditions**: `<condition> <name> <source_id> <url>`
- **interactions**: `<interaction> <source_drug_id> <target_drug_id>`
- **manufacturers**: `<manufacturer> <name>`

#### 🟢 [PubMed](https://www.kaggle.com/datasets/krishnakumarkk/pubmed-knowledge-graph-dataset) *(Kaggle)*
PubMed provides a large dataset of biomedical literature. Due to its size (50GB), it is not included in this project.

### Data Loading and Transformation

1. **Download**: Data is downloaded from various sources using [download_kaggle.py](./download_kaggle.py), [download_geonames.py](./download_geonames.py), and [download_sparql.py](./download_sparql.py).
2. **Transform**: Data is transformed into RDF format using [transform_open_drug.py](./transform_open_drug.py) and [transform_geonames.py](./transform_geonames.py). 
    - The transformation scripts map columns to RDF properties and create triples for each entity.
3. **Merge**: All RDF files are merged into a single RDF file using [merge_rdf.py](./merge_rdf.py).

### Ontology

The ontology defines the structure of the knowledge graph, including classes, properties, and relationships. It ensures consistency and enables reasoning over the data. The ontology is defined in [ontology.ttl](./ontology.ttl) and includes classes such as city, country, and Drug, and properties such as located_in, population, and name.

### Challenges

#### Federated Query Challenges

In `basic_queries_geonames.py`, the federated query is particularly challenging because the `rdfs:label` property in DBpedia does not exactly correspond to the `geo:name` property in Geonames. For example, in Geonames, a city might have `geo:name = "Seaford"`, but in DBpedia, the `rdfs:label` might be `Seaford, Atlanta` or `Seaford, New York`.

This discrepancy makes it difficult to match cities between the two datasets directly. To address this, the query needs to include additional logic to handle these differences, which can make the query more complex and less efficient. This issue highlights the importance of having a consistent ontology and naming conventions across different datasets.

### Reasoning with RDFS

To enhance the knowledge graph, we applied RDFS reasoning to infer new knowledge from the existing data. The ontology defines the relationships between classes and properties, allowing us to infer new information based on these relationships.

#### Ontology Definition

The ontology is defined in [ontology.ttl](./ontology.ttl) and includes the following elements:

- **Classes**: `location`, `city`, `country`, `drug`, `condition`, `interaction`, `manufacturer`
- **Properties**: `capital_of`, `located_in`, `country_code`, `population`, `source_drug_id`, `target_drug_id`, `manufacturer`
- **Unification of Properties**: `dbp:region` and `geo:in_country` are unified under `ex:located_in`

#### Reasoning Process

1. **Load Graph**: Load the RDF data and ontology into a graph.
2. **Apply Reasoning**: Apply RDFS reasoning to infer new knowledge based on the ontology.
3. **Query Graph**: Execute SPARQL queries on the graph before and after reasoning to compare the results.

The reasoning process is implemented in [reasoning.py](./reasoning.py). The script applies RDFS reasoning and compares the results before and after reasoning.

### Conclusion
The integration of SPARQL queries with RDFS reasoning has proven to be an effective method for exploiting the integrated datasets in our knowledge graph. By defining a clear and consistent ontology, we were able to infer new relationships and properties, enriching the data and providing more comprehensive query results. The use of RDFS reasoning allowed us to automatically classify entities into higher-level categories and extend relationships, making the data more interconnected and valuable.

However, there are some limitations. Loading the graph in Python is quite slow, which can be a bottleneck when dealing with large datasets. Additionally, the requests on Geonames that need to call DBpedia are extremely slow, impacting the overall performance of the system.

Future improvements to this project could include optimizing the data loading process and improving the efficiency of federated queries. Integrating additional datasets could further enrich the knowledge graph and provide more comprehensive insights.

### Resources

- [Datasets](#data)
  - Geonames
    - [Geonames Readme.txt](https://download.geonames.org/export/dump/readme.txt)
  - Wikidata
    - [Wikidata Ontology, City](https://www.wikidata.org/wiki/Q515)
  - BDpedia
    - [BDPedia Ontology](https://dbpedia.org/ontology/)
    - [BDPedia Ontology, City](https://dbpedia.org/page/City)
    - [BDPedia Ontology, Country](https://dbpedia.org/page/Country)
  - Open Drug
    - [Open Drug Kaggle](https://www.kaggle.com/datasets/krishnakumarkk/pubmed-knowledge-graph-dataset)
    - [Open Drug Paper](https://ceur-ws.org/Vol-2873/paper10.pdf)
  - PubMed
    - I finally didn't use it.

### TODO

- **Wikidata and DBpedia**: Enhance the data fetching to include more properties such as population, area, and coordinates.
- **Reasoning**: Apply more advanced reasoning techniques to infer new knowledge from the data.
- **Queries**: Develop more complex SPARQL queries to demonstrate the integration of different datasets.
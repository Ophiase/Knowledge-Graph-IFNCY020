import os
from rdflib import Graph, Namespace, RDF, Literal
from rdflib.plugins.sparql import prepareQuery

###################################################################################

RDF_FILE = os.path.join("data", "geonames_knowledge_graph.rdf")
ONTOLOGY_FILE = os.path.join("ontology.ttl")
VERBOSE = True

###################################################################################


def load_graph() -> Graph:
    if VERBOSE:
        print("Load graph")
    g = Graph()
    g.parse(RDF_FILE, format="xml")
    g.parse(ONTOLOGY_FILE, format="turtle")
    return g


def apply_reasoning(g: Graph) -> Graph:
    if VERBOSE:
        print("Apply")
    # automatic?
    return g


def query_graph(g: Graph, query: str):
    results = g.query(query)
    for row in results:
        print(row)


def main():
    g = load_graph()
    g = apply_reasoning(g)

    queries = {
        "inferred_cities": """
        SELECT ?city ?name ?country
        WHERE {
            ?city a <http://example.org/geonames/City> ;
                  <http://example.org/geonames/name> ?name ;
                  <http://example.org/geonames/locatedIn> ?country .
        }
        LIMIT 10
        """,

        "inferred_population": """
        SELECT ?city ?name ?population
        WHERE {
            ?city a <http://example.org/geonames/City> ;
                  <http://example.org/geonames/name> ?name ;
                  <http://example.org/geonames/population> ?population .
        }
        ORDER BY DESC(?population)
        LIMIT 10
        """
    }

    for query_name, query in queries.items():
        if VERBOSE:
            print(f"Executing query: {query_name}\n{query}")
        query_graph(g, query)
        if VERBOSE:
            print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    main()

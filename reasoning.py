import os
from rdflib import Graph, Namespace, RDF, RDFS, Literal

###################################################################################

RDF_FILE = os.path.join("data", "geonames.rdf")
ONTOLOGY_FILE = os.path.join("ontology.ttl")
VERBOSE = True
QUERY_LIMIT = 2

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
        print("Apply reasoning")
    # Apply RDFS reasoning
    inferred_graph = Graph()
    inferred_graph += g
    for s, p, o in g.triples((None, RDF.type, None)):
        if (p, RDF.type, RDF.Property):
            for sp, _, _ in g.triples((p, RDFS.subPropertyOf, None)):
                inferred_graph.add((s, sp, o))
        if (o, RDF.type, RDFS.Class):
            for sc, _, _ in g.triples((s, RDFS.subClassOf, None)):
                inferred_graph.add((s, p, sc))
    return inferred_graph


def query_graph(g: Graph, query: str):
    results = g.query(query)
    for row in results:
        print(row)


def main():
    g = load_graph()
    inferred_g = apply_reasoning(g)

    queries = {
        "inferred_cities": f"""
        SELECT ?city ?name ?country
        WHERE {{
            ?city a <http://example.org/geonames/city> ;
                  <http://example.org/geonames/name> ?name ;
                  <http://example.org/geonames/located_in> ?country .
        }}
        LIMIT {QUERY_LIMIT}
        """,

        "inferred_population": f"""
        SELECT ?city ?name ?population
        WHERE {{
            ?city a <http://example.org/geonames/city> ;
                  <http://example.org/geonames/name> ?name ;
                  <http://example.org/geonames/population> ?population .
        }}
        ORDER BY DESC(?population)
        LIMIT {QUERY_LIMIT}
        """
    }

    for query_name, query in queries.items():
        if VERBOSE:
            print(f"Executing query: {query_name}\n{query}")
        print("Results before reasoning:")
        query_graph(g, query)
        print("Results after reasoning:")
        query_graph(inferred_g, query)
        if VERBOSE:
            print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    main()

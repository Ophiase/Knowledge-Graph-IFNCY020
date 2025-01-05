from rdflib import ConjunctiveGraph, Graph, URIRef

###################################################################################

MINIMAL_QUERIES_ENABLED = True
OTHER_QUERIES_ENABLED = True
QUERY_LIMIT = 10
VERBOSE = True

RDF_FILE = "data/open_drug.rdf"
EX_PREFIX = "http://example.org/"

#########################################

MINIMAL_QUERIES = {
    # # Federated query part 1 (verify the dbpedia ontology)
    #     # Our ontology drugs to try:
    #     # Tolazamide
    #     # Cochliobolus
    #     # Thionicotinamid
    #     # Lacidipine
    #     # Veglin
    # "federated_query_part_1": f"""
    # PREFIX ex: <{EX_PREFIX}>
    # SELECT ?name
    # WHERE {{
    #     SERVICE <https://dbpedia.org/sparql> {{
    #         ?drug a <http://dbpedia.org/ontology/Drug> ;
    #               <http://dbpedia.org/ontology/abstract> ?abstract ;
    #               rdfs:label ?name .
    #         FILTER (lang(?abstract) = 'en' && lang(?name) = 'en')
    #         FILTER (str(?name) = "Tolazamide")
    #     }}
    # }}
    # LIMIT {QUERY_LIMIT}
    # """,

    # # Federated query part 2 (verify our ontology)
    # "federated_query_part_2": f"""
    # PREFIX ex: <{EX_PREFIX}>
    # SELECT ?drug ?name
    # WHERE {{
    #     ?drug a ex:Drug ;
    #           ex:name ?name .
    #     FILTER (str(?name) = "Tolazamide")
    # }}
    # LIMIT {QUERY_LIMIT}
    # """,

    # Federated query
        # Again we use a specifc ?name to fasten the query
    "federated_query": f"""
    PREFIX ex: <{EX_PREFIX}>
    SELECT ?drug ?name ?abstract
    WHERE {{
        SERVICE <https://dbpedia.org/sparql> {{
            ?drug_dbpedia a <http://dbpedia.org/ontology/Drug> ;
                  <http://dbpedia.org/ontology/abstract> ?abstract ;
                  rdfs:label ?name .
            FILTER (lang(?abstract) = 'en' && lang(?name) = 'en')
            FILTER (str(?name) = "Tolazamide")
        }}
        ?drug a ex:Drug ;
              ex:name ?name2 .
        FILTER (STR(?name) = STR(?name2))
    }}
    LIMIT {QUERY_LIMIT}
    """,

    # Query with OPTIONAL
    "optional_query": f"""
    PREFIX ex: <{EX_PREFIX}>
    SELECT ?drug ?name ?wiki_url
    WHERE {{
        ?drug a ex:Drug ;
              ex:name ?name .
        OPTIONAL {{ ?drug ex:wiki_url ?wiki_url }}
    }}
    LIMIT {QUERY_LIMIT}
    """,

    # Query on named graphs
    "named_graph_query": f"""
    PREFIX ex: <{EX_PREFIX}>
    SELECT ?drug ?name
    WHERE {{
        GRAPH <http://example.org/open_drug/graph> {{
            ?drug a ex:Drug ;
                  ex:name ?name .
        }}
    }}
    LIMIT {QUERY_LIMIT}
    """,

    # Query with aggregation
    "aggregation_query": f"""
    PREFIX ex: <{EX_PREFIX}>
    SELECT ?manufacturer (COUNT(?drug) AS ?drugCount)
    WHERE {{
        ?drug a ex:Drug ;
              ex:manufacturer ?manufacturer .
    }}
    GROUP BY ?manufacturer
    ORDER BY DESC(?drugCount)
    LIMIT {QUERY_LIMIT}
    """,

    # Query using path expressions
    "path_expression_query": f"""
    PREFIX ex: <{EX_PREFIX}>
    SELECT ?drug ?name
    WHERE {{
        ?drug (ex:manufacturer|ex:name)+ ?name .
    }}
    LIMIT {QUERY_LIMIT}
    """,

    # Query with MINUS
    "minus_query": f"""
    PREFIX ex: <{EX_PREFIX}>
    SELECT ?drug ?name
    WHERE {{
        ?drug a ex:Drug ;
              ex:name ?name .
        MINUS {{ ?drug ex:wiki_url ?wiki_url }}
    }}
    LIMIT {QUERY_LIMIT}
    """
}

OTHER_QUERIES = {
    "conditions": f"""
    PREFIX ex: <{EX_PREFIX}>
    SELECT ?condition ?name
    WHERE {{
        ?condition a ex:Condition ;
                   ex:name ?name .
    }}
    LIMIT {QUERY_LIMIT}
    """,

    "drugs": f"""
    PREFIX ex: <{EX_PREFIX}>
    SELECT ?drug ?name
    WHERE {{
        ?drug a ex:Drug ;
              ex:name ?name .
    }}
    LIMIT {QUERY_LIMIT}
    """,
    
    "interactions": f"""
    PREFIX ex: <{EX_PREFIX}>
    SELECT ?interaction ?source_drug ?target_drug
    WHERE {{
        ?interaction a ex:Interaction ;
                     ex:source_drug_id ?source_drug ;
                     ex:target_drug_id ?target_drug .
    }}
    LIMIT {QUERY_LIMIT}
    """
}

###################################################################################

def query_graph(graph: Graph, query: str):
    results = graph.query(query, initNs={})
    if len(results) == 0:
        print("No results found.")
    else:
        print(f"Number of results: {len(results)}")
        if VERBOSE:
            for row in results:
                print(row)

def main():
    queries = {}
    if MINIMAL_QUERIES_ENABLED:
        queries.update(MINIMAL_QUERIES)
    if OTHER_QUERIES_ENABLED:
        queries.update(OTHER_QUERIES)

    if VERBOSE:
        print("Build graph..")

    g = Graph()
    g.parse(RDF_FILE, format="xml")

    cg = ConjunctiveGraph()
    graph_uri = URIRef("http://example.org/open_drug/graph")
    for s, p, o in g:
        cg.get_context(graph_uri).add((s, p, o))

    if VERBOSE:
        print(f"ConjunctiveGraph has {len(cg)} triples.")
        print(f"Named graph {graph_uri} has {len(cg.get_context(graph_uri))} triples.")

    for query_name, query in queries.items():
        print(f"Executing query: {query_name}\n{query}")
        
        if query_name == 'named_graph_query':
            query_graph(cg, query)
        else:
            query_graph(g, query)
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()

from rdflib import Graph

###################################################################################

QUERY_LIMIT = 5
VERBOSE = True
RDF_FILE = "data/open_drug.rdf"
EX_PREFIX = "http://example.org/"

#########################################

QUERIES = {
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
    if VERBOSE:
        print("Build graph..")

    g = Graph()
    g.parse(RDF_FILE, format="xml")

    for query_name, query in QUERIES.items():
        print(f"Executing query: {query_name}\n{query}")
        query_graph(g, query)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()

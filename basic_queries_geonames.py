from rdflib import Graph

###################################################################################

MINIMAL_QUERIES_ENABLED = True
OTHER_QUERIES_ENABLED = True
QUERY_LIMIT = 2
VERBOSE = True

RDF_FILE = "data/geonames.rdf"
GEONAMES_PREFIX = "http://example.org/geonames/"

#########################################

MINIMAL_QUERIES = {
    "test" : f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT ?name
    WHERE {{
    SERVICE <https://dbpedia.org/sparql> {{
        ?city a dbo:City ;
            dbo:abstract ?abstract ;
            rdfs:label ?name .
        FILTER (lang(?abstract) = 'en' && lang(?name) = 'en')
        FILTER (STRSTARTS(STR(?name), "Barranq"))
    }}
    }}
    LIMIT {QUERY_LIMIT}
    """,

    "test2" : f"""
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?match
    WHERE {{
        ?city a geo:city ;
              geo:name ?name ;
              geo:population ?population .
        BIND (str(?name) AS ?match)
    }}
    LIMIT {QUERY_LIMIT}
    """,

    # working, but slow if not constrainted
    "federated_query": f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?city ?name ?name2 ?population ?abstract
    WHERE {{
        SERVICE <https://dbpedia.org/sparql> {{
            ?dbo_city a dbo:City ;
                dbo:abstract ?abstract ;
                rdfs:label ?name .
            FILTER (lang(?abstract) = 'en' && lang(?name) = 'en')
            FILTER (STR(?name) = "Barranqueras")
        }}
        ?city a geo:city ;
              geo:name ?name2 ;
              geo:population ?population .
    }}
    LIMIT 1
    """,

    # working
    "optional_query": f"""
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?city ?name ?population ?elevation
    WHERE {{
        ?city a geo:city ;
              geo:name ?name ;
              geo:population ?population .
        OPTIONAL {{ ?city geo:elevation ?elevation }}
    }}
    LIMIT {QUERY_LIMIT}
    """,

    # # not working
    # "named_graph_query": f"""
    # PREFIX geo: <{GEONAMES_PREFIX}>
    # SELECT ?city ?name ?population
    # FROM NAMED <http://example.org/geonames/graph>
    # WHERE {{
    #     GRAPH <http://example.org/geonames/graph> {{
    #         ?city a geo:city ;
    #               geo:name ?name ;
    #               geo:population ?population .
    #     }}
    # }}
    # LIMIT {QUERY_LIMIT}
    # """,

    # working
    "aggregation_query": f"""
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?country (SUM(?population) AS ?totalPopulation)
    WHERE {{
        ?city a geo:city ;
              geo:country_code ?country ;
              geo:population ?population .
    }}
    GROUP BY ?country
    ORDER BY DESC(?totalPopulation)
    LIMIT {QUERY_LIMIT}
    """,

    # working
    "path_expression_query": f"""
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?city ?name
    WHERE {{
        ?city (geo:admin1_code|geo:admin2_code)+ ?admin2_code ;
              geo:name ?name .
    }}
    LIMIT {QUERY_LIMIT}
    """,

    # working
    "minus_query_name_starts_without_b": f"""
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?city ?name
    WHERE {{
        ?city a geo:city ;
              geo:name ?name .
        MINUS {{ ?city geo:name ?name . FILTER (STRSTARTS(?name, "B")) }}
    }}
    LIMIT {QUERY_LIMIT}
    """,
    "minus_query_name_starts_without_s": f"""
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?city ?name
    WHERE {{
        ?city a geo:city ;
              geo:name ?name .
        MINUS {{ ?city geo:name ?name . FILTER (STRSTARTS(?name, "S")) }}
    }}
    LIMIT {QUERY_LIMIT}
    """
}
OTHER_QUERIES = {
    "admin1_codes": f"""
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?admin1_code ?name
    WHERE {{
        ?admin1_code a geo:admin1_code ;
                    geo:name ?name .
    }}
    LIMIT {QUERY_LIMIT}
    """,

    "admin2_codes": f"""
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?admin2Code ?name
    WHERE {{
        ?admin2Code a geo:admin2_code ;
                    geo:name ?name .
    }}
    LIMIT {QUERY_LIMIT}
    """,

    "cities_by_population": f"""
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?city ?name ?population
    WHERE {{
        ?city a geo:city ;
              geo:name ?name ;
              geo:population ?population .
    }}
    ORDER BY DESC(?population)
    LIMIT {QUERY_LIMIT}
    """,

    "country_info": f"""
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?country ?name ?capital
    WHERE {{
        ?country a geo:country_info ;
                 geo:country ?name ;
                 geo:capital ?capital .
    }}
    LIMIT {QUERY_LIMIT}
    """,

    "feature_codes": f"""
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?feature_code ?name ?description
    WHERE {{
        ?feature_code a geo:feature_code ;
                     geo:name ?name ;
                     geo:description ?description .
    }}
    LIMIT {QUERY_LIMIT}
    """,

    "time_zones": f"""
    PREFIX geo: <{GEONAMES_PREFIX}>
    SELECT ?timeZone ?country_code ?gmtOffset
    WHERE {{
        ?timeZone a geo:time_zone ;
                  geo:country_code ?country_code ;
                  geo:gmt_offset ?gmtOffset .
    }}
    LIMIT {QUERY_LIMIT}
    """,
}

###################################################################################


def query_graph(query: str):
    g = Graph()
    g.parse(RDF_FILE, format="xml")
    results = g.query(query, initNs={})
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

    for query_name, query in queries.items():
        print(f"Executing query: {query_name}\n{query}")
        query_graph(query)
        print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    main()

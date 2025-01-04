from rdflib import Graph

###################################################################################

RDF_FILE = "data/geonames_knowledge_graph.rdf"
MINIMAL_QUERIES_ENABLED = False
OTHER_QUERIES_ENABLED = True

#########################################

MINIMAL_QUERIES = {
    "federated_query": """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT ?city ?name ?population ?abstract
    WHERE {
        SERVICE <http://dbpedia.org/sparql> {
            ?city a dbo:City ;
                  dbo:abstract ?abstract .
            FILTER (lang(?abstract) = 'en')
        }
        ?city a <http://example.org/geonames/City> ;
              <http://example.org/geonames/name> ?name ;
              <http://example.org/geonames/population> ?population .
    }
    LIMIT 10
    """,

    "optional_query": """
    SELECT ?city ?name ?population ?elevation
    WHERE {
        ?city a <http://example.org/geonames/City> ;
              <http://example.org/geonames/name> ?name ;
              <http://example.org/geonames/population> ?population .
        OPTIONAL { ?city <http://example.org/geonames/elevation> ?elevation }
    }
    LIMIT 10
    """,

    "named_graph_query": """
    SELECT ?city ?name ?population
    FROM NAMED <http://example.org/geonames/graph>
    WHERE {
        GRAPH <http://example.org/geonames/graph> {
            ?city a <http://example.org/geonames/City> ;
                  <http://example.org/geonames/name> ?name ;
                  <http://example.org/geonames/population> ?population .
        }
    }
    LIMIT 10
    """,

    "aggregation_query": """
    SELECT ?country (SUM(?population) AS ?totalPopulation)
    WHERE {
        ?city a <http://example.org/geonames/City> ;
              <http://example.org/geonames/country_code> ?country ;
              <http://example.org/geonames/population> ?population .
    }
    GROUP BY ?country
    ORDER BY DESC(?totalPopulation)
    LIMIT 10
    """,

    "path_expression_query": """
    SELECT ?city ?name
    WHERE {
        ?city <http://example.org/geonames/admin1_code>/<http://example.org/geonames/admin2_code> ?admin2Code ;
              <http://example.org/geonames/name> ?name .
    }
    LIMIT 10
    """,
    "minus_query": """
    SELECT ?city ?name
    WHERE {
        ?city a <http://example.org/geonames/City> ;
              <http://example.org/geonames/name> ?name .
        MINUS { ?city <http://example.org/geonames/population> ?population }
    }
    LIMIT 10
    """
}
OTHER_QUERIES = {
    "admin1_codes": """
    SELECT ?admin1Code ?name
    WHERE {
        ?admin1Code a <http://example.org/geonames/Admin1Code> ;
                    <http://example.org/geonames/name> ?name .
    }
    LIMIT 10
    """,

    "admin2_codes": """
    SELECT ?admin2Code ?name
    WHERE {
        ?admin2Code a <http://example.org/geonames/Admin2Code> ;
                    <http://example.org/geonames/name> ?name .
    }
    LIMIT 10
    """,

    "cities_by_population": """
    SELECT ?city ?name ?population
    WHERE {
        ?city a <http://example.org/geonames/City> ;
              <http://example.org/geonames/name> ?name ;
              <http://example.org/geonames/population> ?population .
    }
    ORDER BY DESC(?population)
    LIMIT 10
    """,

    "country_info": """
    SELECT ?country ?name ?capital
    WHERE {
        ?country a <http://example.org/geonames/CountryInfo> ;
                 <http://example.org/geonames/Country> ?name ;
                 <http://example.org/geonames/Capital> ?capital .
    }
    LIMIT 10
    """,

    "feature_codes": """
    SELECT ?featureCode ?name ?description
    WHERE {
        ?featureCode a <http://example.org/geonames/FeatureCode> ;
                     <http://example.org/geonames/name> ?name ;
                     <http://example.org/geonames/description> ?description .
    }
    LIMIT 10
    """,

    "time_zones": """
    SELECT ?timeZone ?countryCode ?gmtOffset
    WHERE {
        ?timeZone a <http://example.org/geonames/TimeZone> ;
                  <http://example.org/geonames/country_code> ?countryCode ;
                  <http://example.org/geonames/gmt_offset> ?gmtOffset .
    }
    LIMIT 10
    """,
}

###################################################################################


def query_graph(query: str):
    g = Graph()
    g.parse(RDF_FILE, format="xml")
    results = g.query(query)
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

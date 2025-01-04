from rdflib import Graph

RDF_FILE = "data/geonames_knowledge_graph.rdf"

def query_graph(query: str):
    g = Graph()
    g.parse(RDF_FILE, format="xml")
    results = g.query(query)
    for row in results:
        print(row)

def main():
    queries = [
        """
        SELECT ?admin1Code ?name
        WHERE {
            ?admin1Code a <http://example.org/geonames/Admin1Code> ;
                        <http://example.org/geonames/name> ?name .
        }
        LIMIT 10
        """,

        """
        SELECT ?admin2Code ?name
        WHERE {
            ?admin2Code a <http://example.org/geonames/Admin2Code> ;
                        <http://example.org/geonames/name> ?name .
        }
        LIMIT 10
        """,

        """
        SELECT ?city ?name ?population
        WHERE {
            ?city a <http://example.org/geonames/City> ;
                  <http://example.org/geonames/name> ?name ;
                  <http://example.org/geonames/population> ?population .
        }
        ORDER BY DESC(?population)
        LIMIT 10
        """,

        """
        SELECT ?country ?name ?capital
        WHERE {
            ?country a <http://example.org/geonames/CountryInfo> ;
                     <http://example.org/geonames/Country> ?name ;
                     <http://example.org/geonames/Capital> ?capital .
        }
        LIMIT 10
        """,

        """
        SELECT ?featureCode ?name ?description
        WHERE {
            ?featureCode a <http://example.org/geonames/FeatureCode> ;
                         <http://example.org/geonames/name> ?name ;
                         <http://example.org/geonames/description> ?description .
        }
        LIMIT 10
        """,

        """
        SELECT ?timeZone ?countryCode ?gmtOffset
        WHERE {
            ?timeZone a <http://example.org/geonames/TimeZone> ;
                      <http://example.org/geonames/country_code> ?countryCode ;
                      <http://example.org/geonames/gmt_offset> ?gmtOffset .
        }
        LIMIT 10
        """
    ]

    for query in queries:
        print(f"Executing query:\n{query}")
        query_graph(query)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()

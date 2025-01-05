import os
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD
from typing import Dict, Any

###################################################################################

DATA_FOLDER = os.path.join("data")
RDF_FILE = os.path.join(DATA_FOLDER, "sparql_data.rdf")
VERBOSE = True
MAX_LINES = 100

###################################################################################


def fetch_data(endpoint: str, query: str) -> Dict[str, Any]:
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


#########################################


def fetch_dbpedia_data() -> Dict[str, Any]:
    if VERBOSE:
        print("Downloading data from DBpedia...")

    queries = {
        "cities": f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?city ?cityLabel ?country ?countryLabel WHERE {{
            ?city a dbo:City ;
                rdfs:label ?cityLabel ;
                dbo:country ?country .
            ?country rdfs:label ?countryLabel .
            FILTER (lang(?cityLabel) = 'en' && lang(?countryLabel) = 'en')
        }} LIMIT {MAX_LINES}
        """,
        # "cities": f"""
        # PREFIX dbo: <http://dbpedia.org/ontology/>
        # SELECT ?city ?cityLabel ?country ?countryLabel ?population ?area ?lat ?long WHERE {{
        #     ?city a dbo:City ;
        #           rdfs:label ?cityLabel ;
        #           dbo:country ?country ;
        #           dbo:populationTotal ?population ;
        #           dbo:areaTotal ?area ;
        #           geo:lat ?lat ;
        #           geo:long ?long .
        #     ?country rdfs:label ?countryLabel .
        #     FILTER (lang(?cityLabel) = 'en' && lang(?countryLabel) = 'en')
        # }} LIMIT {MAX_LINES}
        # """,
        # "countries": f"""
        # PREFIX dbo: <http://dbpedia.org/ontology/>
        # SELECT ?country ?countryLabel ?population ?area ?capital ?capitalLabel WHERE {{
        #     ?country a dbo:Country ;
        #              rdfs:label ?countryLabel ;
        #              dbo:populationTotal ?population ;
        #              dbo:areaTotal ?area ;
        #              dbo:capital ?capital .
        #     ?capital rdfs:label ?capitalLabel .
        #     FILTER (lang(?countryLabel) = 'en' && lang(?capitalLabel) = 'en')
        # }} LIMIT {MAX_LINES}
        # """
    }

    results = {}
    for key, query in queries.items():
        results[key] = fetch_data("http://dbpedia.org/sparql", query)
    return results


def fetch_wikidata_data() -> Dict[str, Any]:
    if VERBOSE:
        print("Downloading data from Wikidata...")

    queries = {
        "cities": f"""
        SELECT ?city ?cityLabel ?country ?countryLabel WHERE {{
            ?city wdt:P31/wdt:P279* wd:Q515 ;
                rdfs:label ?cityLabel ;
                wdt:P17 ?country .
            ?country rdfs:label ?countryLabel .
            FILTER (lang(?cityLabel) = 'en' && lang(?countryLabel) = 'en')
        }} LIMIT {MAX_LINES}
        """,
        # "cities": f"""
        # # SELECT ?city ?cityLabel ?country ?countryLabel ?population ?area ?lat ?long WHERE {{
        # #     ?city wdt:P31/wdt:P279* wd:Q515 ;
        # #           rdfs:label ?cityLabel ;
        # #           wdt:P17 ?country ;
        # #           wdt:P1082 ?population ;
        # #           wdt:P2046 ?area ;
        # #           wdt:P625 ?coordinates .
        # #     ?country rdfs:label ?countryLabel .
        # #     BIND(STRAFTER(STR(?coordinates), "Point(") AS ?coords)
        # #     BIND(STRAFTER(?coords, " ") AS ?long)
        # #     BIND(STRBEFORE(?coords, " ") AS ?lat)
        # #     FILTER (lang(?cityLabel) = 'en' && lang(?countryLabel) = 'en')
        # # }} LIMIT {MAX_LINES}
        # # """,
        # "countries": f"""
        # SELECT ?country ?countryLabel ?population ?area ?capital ?capitalLabel WHERE {{
        #     ?country wdt:P31 wd:Q6256 ;
        #              rdfs:label ?countryLabel ;
        #              wdt:P1082 ?population ;
        #              wdt:P2046 ?area ;
        #              wdt:P36 ?capital .
        #     ?capital rdfs:label ?capitalLabel .
        #     FILTER (lang(?countryLabel) = 'en' && lang(?capitalLabel) = 'en')
        # }} LIMIT {MAX_LINES}
        # """
    }

    results = {}
    for key, query in queries.items():
        results[key] = fetch_data("https://query.wikidata.org/sparql", query)
    return results


#########################################


def save_to_rdf(data: Dict[str, Any], g: Graph, EX: Namespace, source: str) -> None:
    for key, results in data.items():
        for result in results["results"]["bindings"]:
            if key == "cities":
                city_uri = URIRef(result["city"]["value"])
                country_uri = URIRef(result["country"]["value"])
                city_label = Literal(result["cityLabel"]["value"])
                country_label = Literal(result["countryLabel"]["value"])
                # population = Literal(result["population"]["value"], datatype=XSD.integer)
                # area = Literal(result["area"]["value"], datatype=XSD.float)
                # lat = Literal(result["lat"]["value"], datatype=XSD.float)
                # long = Literal(result["long"]["value"], datatype=XSD.float)

                g.add((city_uri, RDF.type, EX.City))
                g.add((city_uri, EX.name, city_label))
                g.add((city_uri, EX.locatedIn, country_uri))
                # g.add((city_uri, EX.population, population))
                # g.add((city_uri, EX.area, area))
                # g.add((city_uri, EX.latitude, lat))
                # g.add((city_uri, EX.longitude, long))
                g.add((country_uri, RDF.type, EX.Country))
                g.add((country_uri, EX.name, country_label))
                g.add((city_uri, EX.source, Literal(source)))

            elif key == "countries":
                country_uri = URIRef(result["country"]["value"])
                capital_uri = URIRef(result["capital"]["value"])
                country_label = Literal(result["countryLabel"]["value"])
                capital_label = Literal(result["capitalLabel"]["value"])
                population = Literal(result["population"]["value"], datatype=XSD.integer)
                area = Literal(result["area"]["value"], datatype=XSD.float)

                g.add((country_uri, RDF.type, EX.Country))
                g.add((country_uri, EX.name, country_label))
                g.add((country_uri, EX.population, population))
                g.add((country_uri, EX.area, area))
                g.add((country_uri, EX.capital, capital_uri))
                g.add((capital_uri, RDF.type, EX.City))
                g.add((capital_uri, EX.name, capital_label))
                g.add((country_uri, EX.source, Literal(source)))

###################################################################################


def main() -> None:
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    g = Graph()
    EX = Namespace("http://example.org/sparql/")
    g.bind("ex", EX)

    dbpedia_data = fetch_dbpedia_data()
    save_to_rdf(dbpedia_data, g, EX, "DBpedia")

    wikidata_data = fetch_wikidata_data()
    save_to_rdf(wikidata_data, g, EX, "Wikidata")

    g.serialize(destination=RDF_FILE, format='xml')

    if VERBOSE:
        print(f"Data saved to {RDF_FILE}")


if __name__ == '__main__':
    main()

from SPARQLWrapper import SPARQLWrapper, JSON

###################################################################################


MAX_LINES = 3
VERBOSE = True

###################################################################################


def fetch_dbpedia_data(query: str):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def fetch_wikidata_data(query: str):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def download_dbpedia_data() -> None:
    if VERBOSE:
        print("download dbpedia...")

    query = """
    SELECT ?city ?cityLabel ?country ?countryLabel WHERE {
        ?city a dbo:City ;
              rdfs:label ?cityLabel ;
              dbo:country ?country .
        ?country rdfs:label ?countryLabel .
        FILTER (lang(?cityLabel) = 'fr' && lang(?countryLabel) = 'fr')
    } LIMIT
    """ + str(MAX_LINES)

    results = fetch_dbpedia_data(query)
    print(f"\n{results}\n")


def download_wikidata_data() -> None:
    if VERBOSE:
        print("download wikidata...")

    query = """
    SELECT ?city ?cityLabel ?country ?countryLabel WHERE {
        ?city wdt:P31/wdt:P279* wd:Q515 ;
              rdfs:label ?cityLabel ;
              wdt:P17 ?country .
        ?country rdfs:label ?countryLabel .
        FILTER (lang(?cityLabel) = 'fr' && lang(?countryLabel) = 'fr')
    } LIMIT
    """ + str(MAX_LINES)

    results = fetch_wikidata_data(query)
    print(f"\n{results}\n")

###################################################################################


def main() -> None:
    download_wikidata_data()
    download_dbpedia_data()


if __name__ == '__main__':
    main()

from rdflib import Graph

RDF_FILE = "data/open_drug.rdf"

def query_graph(query: str):
    g = Graph()
    g.parse(RDF_FILE, format="xml")
    results = g.query(query)
    for row in results:
        print(row)

def main():
    queries = [
        """
        SELECT ?condition ?name
        WHERE {
            ?condition a <http://example.org/Condition> ;
                       <http://example.org/name> ?name .
        }
        LIMIT 10
        """,

        """
        SELECT ?drug ?name
        WHERE {
            ?drug a <http://example.org/Drug> ;
                  <http://example.org/name> ?name .
        }
        LIMIT 10
        """,
        
        """
        SELECT ?interaction ?source_drug ?target_drug
        WHERE {
            ?interaction a <http://example.org/Interaction> ;
                         <http://example.org/source_drug_id> ?source_drug ;
                         <http://example.org/target_drug_id> ?target_drug .
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

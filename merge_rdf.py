import os
from rdflib import Graph

###################################################################################

DATA_FOLDER = os.path.join("data")
OUTPUT_FILE = os.path.join(DATA_FOLDER, "merged.rdf")
VERBOSE = True

###################################################################################


def merge_rdf_files(output_file: str, *input_files: str) -> None:
    g = Graph()
    for input_file in input_files:
        if VERBOSE:
            print(f"Merging {input_file}...")
        g.parse(input_file, format="xml")
    g.serialize(destination=output_file, format='xml')
    if VERBOSE:
        print(f"Data saved to {output_file}")


def main() -> None:
    rdf_files = [
        os.path.join(DATA_FOLDER, "open_drug.rdf"),
        os.path.join(DATA_FOLDER, "geonames.rdf"),
        os.path.join(DATA_FOLDER, "sparql_data.rdf")
    ]
    merge_rdf_files(OUTPUT_FILE, *rdf_files)


if __name__ == '__main__':
    main()

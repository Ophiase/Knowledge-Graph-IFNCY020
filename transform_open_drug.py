import os
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from typing import Dict, Tuple

###################################################################################

DATA_FOLDER = os.path.join("data", "open_drug")
OUTPUT_FILE = os.path.join("data", "open_drug.rdf")
VERBOSE = True
LINE_LIMIT = 10000

###################################################################################


def create_graph() -> Tuple[Graph, Namespace]:
    g = Graph()
    EX = Namespace("http://example.org/")
    g.bind("ex", EX)
    return g, EX


def add_triples(g: Graph, df: pd.DataFrame, subject_class: URIRef, subject_prefix: str, properties: Dict[URIRef, str]) -> None:
    for _, row in df.iterrows():
        subject = URIRef(f"{subject_prefix}{row['id']}")
        g.add((subject, RDF.type, subject_class))
        for prop, col in properties.items():
            if pd.notna(row[col]):
                g.add((subject, prop, Literal(row[col])))


def process_condition(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.Condition, EX.condition, {
        EX.name: "name",
        EX.source_id: "source_id",
        EX.url: "url"
    })


def process_drug(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.Drug, EX.drug, {
        EX.name: "name",
        EX.wiki_url: "wiki_url",
        EX.drugbank_url: "drugbank_url"
    })


def process_interaction(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    for _, row in df.iterrows():
        interaction = URIRef(f"{EX.interaction}{row['id']}")
        g.add((interaction, RDF.type, EX.Interaction))
        g.add((interaction, EX.source_drug_id, URIRef(
            f"{EX.drug}{row['source_drug_id']}")))
        g.add((interaction, EX.target_drug_id, URIRef(
            f"{EX.drug}{row['target_drug_id']}")))


def process_manufacturer(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.Manufacturer, EX.manufacturer, {
        EX.name: "name"
    })


def process_price(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.Price, EX.price, {
        EX.product_id: "product_id",
        EX.store_id: "store_id",
        EX.type: "type",
        EX.price: "price",
        EX.url: "url"
    })


def process_product(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.Product, EX.product, {
        EX.source_id: "source_id",
        EX.drug_id: "drug_id",
        EX.name: "name",
        EX.url: "url",
        EX.type: "type",
        EX.n_reviews: "n_reviews",
        EX.manufacturer_id: "manufacturer_id"
    })


def process_source(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.Source, EX.source, {
        EX.name: "name",
        EX.url: "url"
    })


def process_store(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.Store, EX.store, {
        EX.name: "name"
    })


def process_treatment(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    for _, row in df.iterrows():
        treatment = URIRef(f"{EX.treatment}{row['id']}")
        g.add((treatment, RDF.type, EX.Treatment))
        g.add((treatment, EX.source_id, URIRef(
            f"{EX.source}{row['source_id']}")))
        g.add((treatment, EX.condition_id, URIRef(
            f"{EX.condition}{row['condition_id']}")))
        g.add((treatment, EX.drug_id, URIRef(f"{EX.drug}{row['drug_id']}")))

###################################################################################


def process_file(g: Graph, EX: Namespace, file_name: str, file_path: str) -> None:
    if VERBOSE:
        print(f"Processing {file_name}...")

    df = pd.read_csv(file_path, nrows=LINE_LIMIT)

    match file_name:
        case "condition.csv":
            process_condition(g, EX, df)
        case "drug.csv":
            process_drug(g, EX, df)
        case "interaction.csv":
            process_interaction(g, EX, df)
        case "manufacturer.csv":
            process_manufacturer(g, EX, df)
        case "price.csv":
            process_price(g, EX, df)
        case "product.csv":
            process_product(g, EX, df)
        case "source.csv":
            process_source(g, EX, df)
        case "store.csv":
            process_store(g, EX, df)
        case "treatment.csv":
            process_treatment(g, EX, df)

###################################################################################


def main():
    g, EX = create_graph()
    for file_name in os.listdir(DATA_FOLDER):
        file_path = os.path.join(DATA_FOLDER, file_name)
        process_file(g, EX, file_name, file_path)
    g.serialize(destination=OUTPUT_FILE, format='xml')


if __name__ == "__main__":
    main()

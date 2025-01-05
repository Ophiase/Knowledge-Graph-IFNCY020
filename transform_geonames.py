import os
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from typing import Dict, Tuple

###################################################################################

DATA_FOLDER = os.path.join("data", "geonames")
FEATURES_FOLDER = os.path.join(DATA_FOLDER, "features")
OUTPUT_FILE = os.path.join("data", "geonames.rdf")
VERBOSE = True
LINE_LIMIT = 1000
LINE_LIMIT_FEATURE = 100

###################################################################################


def create_graph() -> Tuple[Graph, Namespace]:
    g = Graph()
    EX = Namespace("http://example.org/geonames/")
    g.bind("ex", EX)
    return g, EX


def add_triples(g: Graph, df: pd.DataFrame, subject_class: URIRef, subject_prefix: str, properties: Dict[URIRef, str], id_column: str) -> None:
    for _, row in df.iterrows():
        subject = URIRef(f"{subject_prefix}{row[id_column]}")
        g.add((subject, RDF.type, subject_class))
        for prop, col in properties.items():
            if pd.notna(row[col]):
                g.add((subject, prop, Literal(row[col])))


def process_admin1_codes(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.admin1_code, EX.admin1_code, {
        EX.code: "code",
        EX.name: "name",
        EX.name_ascii: "name_ascii",
        EX.geoname_id: "geoname_id"
    }, "code")


def process_admin2_codes(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.admin2_code, EX.admin2_code, {
        EX.code: "code",
        EX.name: "name",
        EX.ascii_name: "ascii_name",
        EX.geoname_id: "geoname_id"
    }, "code")


def process_admin5_codes(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.admin5_code, EX.admin5_code, {
        EX.geoname_id: "geoname_id",
        EX.adm5code: "adm5code"
    }, "geoname_id")


def process_alternate_names(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.alternate_name, EX.alternate_name, {
        EX.alternate_name_id: "alternateNameId",
        EX.geoname_id: "geoname_id",
        EX.iso_language: "iso_language",
        EX.alternate_name: "alternate_name"
    }, "alternateNameId")


def process_cities(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.city, EX.city, {
        EX.geoname_id: "geoname_id",
        EX.name: "name",
        EX.ascii_name: "ascii_name",
        EX.alternate_names: "alternate_names",
        EX.latitude: "latitude",
        EX.longitude: "longitude",
        EX.feature_class: "feature_class",
        EX.feature_code: "feature_code",
        EX.country_code: "country_code",
        EX.cc2: "cc2",
        EX.admin1_code: "admin1_code",
        EX.admin2_code: "admin2_code",
        EX.admin3_code: "admin3_code",
        EX.admin4_code: "admin4_code",
        EX.population: "population",
        EX.elevation: "elevation",
        EX.dem: "dem",
        EX.timezone: "timezone",
        EX.modification_date: "modification_date"
    }, "geoname_id")


def process_country_info(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.country_info, EX.country_info, {
        EX.iso: "iso",
        EX.iso3: "iso3",
        EX.iso_numeric: "iso-numeric",
        EX.fips: "fips",
        EX.country: "country",
        EX.capital: "capital",
        EX.area_in_sq_km: "area_in_sq_km",
        EX.population: "population",
        EX.continent: "continent",
        EX.tld: "tld",
        EX.currency_code: "currency_code",
        EX.currency_name: "currency_name",
        EX.phone: "phone",
        EX.postal_code_format: "postal_code_format",
        # EX.postal_code_regex: "Postal Code Regex",
        # EX.languages: "Languages",
        # EX.geoname_id: "geoname_id",
        # EX.neighbours: "neighbours",
        # EX.equivalent_fips_code: "EquivalentFipsCode"
    }, "iso")


def process_feature_codes(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.feature_code, EX.feature_code, {
        EX.code: "code",
        EX.name: "name",
        EX.description: "description"
    }, "code")


def process_hierarchy(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.hierarchy, EX.hierarchy, {
        EX.parent_id: "parent_id",
        EX.child_id: "child_id",
        EX.type: "type"
    }, "parent_id")


def process_iso_language_codes(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    df.columns = [col.replace(" ", "_") for col in df.columns]
    add_triples(g, df, EX.iso_language_code, EX.iso_language_code, {
        EX.iso_639_3: "iso_639_3",
        EX.iso_639_2: "iso_639_2",
        EX.iso_639_1: "iso_639_1",
        EX.language_name: "language_name"
    }, "iso_639_3")


def process_time_zones(g: Graph, EX: Namespace, df: pd.DataFrame) -> None:
    add_triples(g, df, EX.time_zone, EX.time_zone, {
        EX.country_code: "country_code",
        EX.timezone_id: "time_zone_id",
        EX.gmt_offset: "gmt_offset_1_jan_2025",
        EX.dst_offset: "dst_offset_1_jul_2025",
        EX.raw_offset: "raw_offset_independant_of_dst"
    }, "country_code")


def process_features(g: Graph, EX: Namespace, file_path: str) -> None:
    df = pd.read_csv(file_path, delimiter='\t', header=None, names=[
        "geoname_id", "name", "ascii_name", "alternate_names", "latitude", "longitude",
        "feature_class", "feature_code", "country_code", "cc2", "admin1_code", "admin2_code",
        "admin3_code", "admin4_code", "population", "elevation", "dem", "timezone", "modification_date"
    ], nrows=LINE_LIMIT_FEATURE, comment='#', on_bad_lines='skip')
    
    add_triples(g, df, EX.feature, EX.feature, {
        EX.geoname_id: "geoname_id",
        EX.name: "name",
        EX.ascii_name: "ascii_name",
        EX.alternate_names: "alternate_names",
        EX.latitude: "latitude",
        EX.longitude: "longitude",
        EX.feature_class: "feature_class",
        EX.feature_code: "feature_code",
        EX.country_code: "country_code",
        EX.cc2: "cc2",
        EX.admin1_code: "admin1_code",
        EX.admin2_code: "admin2_code",
        EX.admin3_code: "admin3_code",
        EX.admin4_code: "admin4_code",
        EX.population: "population",
        EX.elevation: "elevation",
        EX.dem: "dem",
        EX.timezone: "timezone",
        EX.modification_date: "modification_date"
    }, "geoname_id")

###################################################################################


def process_file(g: Graph, EX: Namespace, file_name: str, file_path: str) -> None:
    if VERBOSE:
        print(f"Processing {file_name}...")

    file_columns = {
        "admin1CodesASCII.txt": ["code", "name", "name_ascii", "geoname_id"],
        "admin2Codes.txt": ["code", "name", "ascii_name", "geoname_id"],
        "adminCode5.txt": ["geoname_id", "adm5code"],
        "alternateNamesV2.txt": ["alternateNameId", "geoname_id", "iso_language", "alternate_name", "is_preferred_name", "is_short_name", "is_colloquial", "is_historic", "from", "to"],
        "cities500.txt": ["geoname_id", "name", "ascii_name", "alternate_names", "latitude", "longitude", "feature_class", "feature_code", "country_code", "cc2", "admin1_code", "admin2_code", "admin3_code", "admin4_code", "population", "elevation", "dem", "timezone", "modification_date"],
        "cities1000.txt": ["geoname_id", "name", "ascii_name", "alternate_names", "latitude", "longitude", "feature_class", "feature_code", "country_code", "cc2", "admin1_code", "admin2_code", "admin3_code", "admin4_code", "population", "elevation", "dem", "timezone", "modification_date"],
        "cities5000.txt": ["geoname_id", "name", "ascii_name", "alternate_names", "latitude", "longitude", "feature_class", "feature_code", "country_code", "cc2", "admin1_code", "admin2_code", "admin3_code", "admin4_code", "population", "elevation", "dem", "timezone", "modification_date"],
        "cities15000.txt": ["geoname_id", "name", "ascii_name", "alternate_names", "latitude", "longitude", "feature_class", "feature_code", "country_code", "cc2", "admin1_code", "admin2_code", "admin3_code", "admin4_code", "population", "elevation", "dem", "timezone", "modification_date"],
        "countryInfo.txt": ["iso", "iso3", "iso-numeric", "fips", "country", "capital", "area_in_sq_km", "population", "continent", "tld", "currency_code", "currency_name", "phone", "postal_code_format"],# "Postal Code Regex", "Languages", "geoname_id", "neighbours", "EquivalentFipsCode"],
        "featureCodes_en.txt": ["code", "name", "description"],
        "hierarchy.txt": ["parent_id", "child_id", "type"],
        "iso-languagecodes.txt": ["iso_639_3", "iso_639_2", "iso_639_1", "language_name"],
        "timeZones.txt": ["country_code", "time_zone_id", "gmt_offset_1_jan_2025", "dst_offset_1_jul_2025", "raw_offset_independant_of_dst"]
    }

    if file_name in file_columns:
        df = pd.read_csv(file_path, delimiter='\t', nrows=LINE_LIMIT, header=None, comment='#', on_bad_lines='skip')
        df.columns = file_columns[file_name]
        match file_name:
            case "admin1CodesASCII.txt":
                process_admin1_codes(g, EX, df)
            case "admin2Codes.txt":
                process_admin2_codes(g, EX, df)
            case "adminCode5.txt":
                process_admin5_codes(g, EX, df)
            case "alternateNamesV2.txt":
                process_alternate_names(g, EX, df)
            case "cities500.txt" | "cities1000.txt" | "cities5000.txt" | "cities15000.txt":
                process_cities(g, EX, df)
            case "countryInfo.txt":
                process_country_info(g, EX, df)
            case "featureCodes_en.txt":
                process_feature_codes(g, EX, df)
            case "hierarchy.txt":
                process_hierarchy(g, EX, df)
            case "iso-languagecodes.txt":
                df = df.drop(0)
                process_iso_language_codes(g, EX, df)
            case "timeZones.txt":
                process_time_zones(g, EX, df)
    else:
        if VERBOSE:
            print(f"File {file_name} not recognized, skipping.")


def process_feature_files(g: Graph, EX: Namespace) -> None:
    if VERBOSE:
        print("Processing feature folder")
    for file_name in sorted(os.listdir(FEATURES_FOLDER)):
        if VERBOSE:
            print(f"{file_name}, ", end="", flush=True)
        file_path = os.path.join(FEATURES_FOLDER, file_name)
        if file_name.endswith(".txt"):
            process_features(g, EX, file_path)

###################################################################################


def main():
    g, EX = create_graph()
    for file_name in os.listdir(DATA_FOLDER):
        file_path = os.path.join(DATA_FOLDER, file_name)
        process_file(g, EX, file_name, file_path)
    process_feature_files(g, EX)
    print("serialize...")
    g.serialize(destination=OUTPUT_FILE, format='xml')
    print("done")


if __name__ == "__main__":
    main()

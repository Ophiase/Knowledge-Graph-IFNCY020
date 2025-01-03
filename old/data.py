import os
import requests
from rdflib import Graph

DATA_FOLDER = 'rdf_data'
os.makedirs(DATA_FOLDER, exist_ok=True)

datasets = {
    'geozones.rdf': 'https://www.data.gouv.fr/api/1/site/catalog.rdf?page=390&page_size=100i'
}

def download_file(url, dest):
    response = requests.get(url)
    if response.status_code == 200:
        with open(dest, 'wb') as f:
            f.write(response.content)
        print(f'Téléchargé : {dest}')
    else:
        print(f'Échec du téléchargement : {url}')

def validate_rdf(file_path):
    try:
        g = Graph()
        g.parse(file_path)
        print(f'Validation réussie : {file_path}')
        return True
    except Exception as e:
        print(f'Erreur de validation pour {file_path} : {e}')
        return False

def convert_to_turtle(file_path):
    g = Graph()
    g.parse(file_path)
    turtle_path = file_path.replace('.rdf', '.ttl')
    g.serialize(destination=turtle_path, format='turtle')
    print(f'Converti en Turtle : {turtle_path}')
    return turtle_path

def merge_graphs(file_paths, output_path):
    merged_graph = Graph()
    for file_path in file_paths:
        g = Graph()
        g.parse(file_path)
        merged_graph += g
    merged_graph.serialize(destination=output_path, format='turtle')
    print(f'Graphes fusionnés dans : {output_path}')

def main() -> None :    
    for filename, url in datasets.items():
        file_path = os.path.join(DATA_FOLDER, filename)
        download_file(url, file_path)

    turtle_files = []
    for filename in datasets.keys():
        file_path = os.path.join(DATA_FOLDER, filename)
        if validate_rdf(file_path):
            turtle_file = convert_to_turtle(file_path)
            turtle_files.append(turtle_file)

    if turtle_files:
        output_file = os.path.join(DATA_FOLDER, 'merged_data.ttl')
        merge_graphs(turtle_files, output_file)

if __name__=="__main__":
    main()
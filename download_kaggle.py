import kagglehub
import pandas as pd
import os
import numpy as np
import shutil


def extract(target_folder: str, kaggle_data: str) -> str:
    original_folder = kagglehub.dataset_download(kaggle_data)

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for item in os.listdir(original_folder):
        s = os.path.join(original_folder, item)
        d = os.path.join(target_folder, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    return target_folder


def main() -> None:
    for target_folder, kaggle_data in [
        # ('pubmed', "krishnakumarkk/pubmed-knowledge-graph-dataset"), # too heavy
        ("open_drug", "mannbrinson/open-drug-knowledge-graph")
    ]:
        extract(os.path.join("data", target_folder), kaggle_data)


if __name__ == "__main__":
    main()

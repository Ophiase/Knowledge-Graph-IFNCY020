import kagglehub
import pandas as pd
import os
import numpy as np
import shutil

TARGET_FOLDER = os.path.join("data", "open_drug")

def extract(target_folder: str = TARGET_FOLDER) -> str:
    original_folder = kagglehub.dataset_download("mannbrinson/open-drug-knowledge-graph")
    
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
    extract()

if __name__ == "__main__":
    main()
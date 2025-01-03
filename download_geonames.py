import requests
import os
import zipfile
from typing import List

###################################################################################

DEFAULT_DOWNLOAD_FOLDER = "data/geonames"
BASE_URL = "https://download.geonames.org/export/dump/"
FILES = [
    "allCountries.zip",
    "cities500.zip",
    "cities1000.zip",
    "cities5000.zip",
    "cities15000.zip",
    "alternateNamesV2.zip",
    "admin1CodesASCII.txt",
    "admin2Codes.txt",
    "iso-languagecodes.txt",
    "featureCodes.txt",
    "timeZones.txt",
    "countryInfo.txt",
    "hierarchy.zip",
    "adminCode5.zip"
]
FEATURES_FILES = [
    "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AN", "AO", "AQ", "AR", "AS", "AT", "AU", "AW",
    "AX", "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM", "BN", "BO",
    "BQ", "BR", "BS", "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI",
    "CK", "CL", "CM", "CN", "CO", "CR", "CS", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ",
    "DK", "DM", "DO", "DZ", "EC", "EE", "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM",
    "FO", "FR", "GA", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ",
    "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM", "HN", "HR", "HT", "HU", "ID", "IE", "IL",
    "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JM", "JO", "JP", "KE", "KG", "KH", "KI",
    "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS", "LT",
    "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK", "ML", "MM", "MN", "MO",
    "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA", "NC", "NE", "NF",
    "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG", "PH", "PK",
    "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW", "SA",
    "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR", "SS",
    "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN",
    "TO", "TR", "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE",
    "VG", "VI", "VN", "VU", "WF", "WS", "XK", "YE", "YT", "YU", "ZA", "ZM", "ZW"
]

###################################################################################


def download_file(url: str, dest_folder: str) -> None:
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(dest_folder, url.split("/")[-1])
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
    else:
        print(f"Failed to download {url}")


def download_files(file_list: List[str], dest_folder: str = DEFAULT_DOWNLOAD_FOLDER) -> None:
    for file_name in file_list:
        file_url = BASE_URL + file_name
        download_file(file_url, dest_folder)


def unzip_files(dest_folder: str = DEFAULT_DOWNLOAD_FOLDER) -> None:
    for file_name in os.listdir(dest_folder):
        if file_name.endswith(".zip"):
            file_path = os.path.join(dest_folder, file_name)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(dest_folder)
            os.remove(file_path)

###################################################################################

def main() -> None:
    ALL_FILES : List[str] = FILES + [f"{file}.zip" for file in FEATURES_FILES]
    download_files(FILES)
    unzip_files()

if __name__ == "__main__":
    main()

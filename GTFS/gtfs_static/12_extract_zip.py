import csv
import os
import zipfile

def extract_zip(zip_path, extract_to):
    print(f"📦 Extracting {zip_path} to {extract_to}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("✅ Extraction complete")


def main():
    directory = os.path.dirname(os.path.abspath(__file__))

    zip_path = os.path.join(directory, "gtfs.zip")

    extract_zip(zip_path, directory)

if __name__ == "__main__":
    main()

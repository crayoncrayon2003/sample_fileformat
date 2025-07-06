import os
import requests

def download_zip(url, save_path):
    print(f"Downloading ZIP from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"Saved to {save_path}")

def main():
    directory = os.path.dirname(os.path.abspath(__file__))

    gtfs_url = "https://example.com/gtfs_static.zip"
    zip_path = os.path.join(directory, "gtfs.zip")

    download_zip(gtfs_url, zip_path)

if __name__ == "__main__":
    main()

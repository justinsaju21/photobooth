import urllib.request
import os

os.makedirs("assets", exist_ok=True)

fonts = {
    "assets/Lato-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/lato/Lato-Regular.ttf",
    "assets/PlayfairDisplay-Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/static/PlayfairDisplay-Bold.ttf"
}

for path, url in fonts.items():
    print(f"Downloading {url} to {path}...")
    try:
        urllib.request.urlretrieve(url, path)
        print("Success.")
    except Exception as e:
        print(f"Failed: {e}")

import requests
import os

FONTS = {
    "PlayfairDisplay-Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay-Bold.ttf",
    "CourierPrime-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/courierprime/CourierPrime-Regular.ttf",
    "GreatVibes-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/greatvibes/GreatVibes-Regular.ttf",
    "Oswald-Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/oswald/Oswald-Bold.ttf",
    "Roboto-Light.ttf": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Light.ttf",
    "UnifrakturMaguntia-Book.ttf": "https://github.com/google/fonts/raw/main/ofl/unifrakturmaguntia/UnifrakturMaguntia-Book.ttf",
    "PatrickHand-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/patrickhand/PatrickHand-Regular.ttf"
}

ASSET_DIR = "c:\\Users\\justi\\.gemini\\antigravity\\scratch\\Photobooth\\assets"

if not os.path.exists(ASSET_DIR):
    os.makedirs(ASSET_DIR)

print(f"Downloading fonts to {ASSET_DIR}...")

for filename, url in FONTS.items():
    filepath = os.path.join(ASSET_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Downloading {filename}...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✅ Saved {filename}")
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
    else:
        print(f"⏭️ {filename} already exists.")

print("Font download complete.")

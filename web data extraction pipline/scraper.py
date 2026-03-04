import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://quotes.toscrape.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def fetch_page(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise

html = fetch_page(URL)
soup = BeautifulSoup(html, "html.parser")

quotes = soup.find_all("div", class_="quote")

dataset = []

for quote in quotes:
    text = quote.find("span", class_="text").text.strip()
    author = quote.find("small", class_="author").text.strip()
    tags = [tag.text for tag in quote.find_all("a", class_="tag")]

    dataset.append({
        "quote": text,
        "author": author,
        "tags": ", ".join(tags)
    })

df = pd.DataFrame(dataset)
df.to_csv("quotes_dataset.csv", index=False)

print("Dataset exported successfully")

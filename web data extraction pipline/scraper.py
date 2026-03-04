import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://quotes.toscrape.com"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

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

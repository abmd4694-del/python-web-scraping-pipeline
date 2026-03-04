import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://quotes.toscrape.com/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.find_all("div", class_="quote")

data = []

for q in quotes:
    text = q.find("span", class_="text").text
    author = q.find("small", class_="author").text
    tags = [tag.text for tag in q.find("a", class_="tag")]

    data.append({
        "quote": text,
        "author": author,
        "tags": ", ".join(tags)
    })

# Ensure output directory exists before saving
os.makedirs("output", exist_ok=True)

df = pd.DataFrame(data)
df.to_csv("output/quotes.csv", index=False)

print("Data saved to output/quotes.csv")

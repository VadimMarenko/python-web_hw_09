import json
from time import sleep

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import seeds

# import search_quotes
starts_url = "https://quotes.toscrape.com/"
HTTP_STATUS_OK = 200
NUM_COLS = 100


def quotes_json():
    all_quotes = []
    all_urls = set()

    for p in tqdm(range(1, 10 + 1), desc="Pages", ncols=NUM_COLS):
        url = f"{starts_url}page/{p}"
        response = requests.get(url)
        if response.status_code == HTTP_STATUS_OK:
            sleep(3)
            soup = BeautifulSoup(response.text, "lxml")

            quotes = soup.find_all("span", class_="text")
            authors = soup.find_all("small", class_="author")
            about = soup.find_all("div", class_="quote")[1]
            tags = soup.find_all("div", class_="tags")

            for a in soup.select("[href^='/author']"):
                all_urls.add(a["href"])

            for i in range(0, len(quotes)):
                tagsforquote = tags[i].find_all("a", class_="tag")
                all_tags = []
                for tagforquote in tagsforquote:
                    all_tags.append(tagforquote.text)

                all_quotes.append(
                    {
                        "tags": all_tags,
                        "author": authors[i].text,
                        "quote": quotes[i].text,
                    }
                )

    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(all_quotes, f, ensure_ascii=False)
    return all_urls


def authors_json(urls):
    all_authors = []

    for url in tqdm(urls, desc="Data Processing", ncols=NUM_COLS):
        link = f"{starts_url}{url}"
        response = requests.get(link)
        if response.status_code == HTTP_STATUS_OK:
            sleep(3)

            soup = BeautifulSoup(response.text, "lxml")
            author = soup.find("h3", class_="author-title")
            born_date = soup.find("span", class_="author-born-date")
            born_location = soup.find("span", class_="author-born-location")
            description = soup.find("div", class_="author-description").text.strip()
            authors_item = {
                "fullname": author.text,
                "born_date": born_date.text,
                "born_location": born_location.text,
                "description": description,
            }
            if authors_item not in all_authors:
                all_authors.append(authors_item)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(all_authors, f, ensure_ascii=False)


if __name__ == "__main__":
    urls = quotes_json()
    authors_json(urls)
    seeds.loads_json_to_db()

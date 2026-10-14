
import requests
from bs4 import BeautifulSoup
import json

URL = "https://news.ycombinator.com/"

def scrape_headlines():
    try:
        print("Fetching technology headlines...")

        response = requests.get(
            URL,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        headlines = []

        for item in soup.select("span.titleline > a"):
            title = item.get_text(strip=True)
            link = item.get("href", "")

            if title and link:
                headlines.append({
                    "headline": title,
                    "url": link
                })

        if not headlines:
            print("No headlines found.")
            return

        with open("headlines.json", "w", encoding="utf-8") as file:
            json.dump(headlines, file, indent=4, ensure_ascii=False)

        with open("headlines.txt", "w", encoding="utf-8") as file:
            for number, item in enumerate(headlines, start=1):
                file.write(f"{number}. {item['headline']}\n")
                file.write(f"Link: {item['url']}\n\n")

        print(f"Successfully extracted {len(headlines)} headlines!")
        print("Saved to headlines.json and headlines.txt")

    except requests.exceptions.RequestException as error:
        print("Website connection error:", error)

    except OSError as error:
        print("File saving error:", error)


if __name__ == "__main__":
    scrape_headlines()

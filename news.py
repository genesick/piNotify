import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from urllib.parse import urljoin


def webscrape_news(url):
    # Send a GET request to the URL and get the page content
    response = requests.get(url)
    content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = bs(content, "html.parser")

    # Find all the article links on the page
    article_links = soup.find_all("a", {"class": "c-teaser__link"})
    print("hiiiii")

    for article_link in article_links:
        article_url = urljoin(url, article_link["href"])
        article_response = requests.get(article_url)
        article_content = article_response.content
        article_soup = bs(article_content, "html.parser")
        
        article_title = article_soup.find("h1", {"class": "c-article__heading"}).get_text()
        article_time = article_soup.find("time", {"itemprop": "datePublished"})["datetime"]
        publication_datetime = datetime.fromisoformat(article_time[:-1])
        
        article_category = article_soup.find("span", {"class": "c-article__category"}).text.strip()
        if article_category == "Göteborg":
            if publication_datetime.time() < datetime.strptime('10:00', '%H:%M').time() and publication_datetime.time() >= datetime.strptime('00:00', '%H:%M').time():
                print(f"{article_title}")
            

if __name__ == "__main__":
    url = "https://www.gp.se"
    webscrape_news(url)

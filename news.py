import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta, time
from urllib.parse import urljoin
import pyshorteners
from twiliotest import piNotifier


def webscrape_news(url):
    missed_news = list()
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)

    # Send a GET request to the URL and get the page content
    response = requests.get(url)
    content = response.content
    
    article_date = None

    # Parse the HTML content using BeautifulSoup
    soup = bs(content, "html.parser")

    # Find all the article links on the page
    article_links = soup.find_all("a", {"class": "c-teaser__link"})

    for article_link in article_links:
        article_url = urljoin(url, article_link["href"])
        article_response = requests.get(article_url)
        article_content = article_response.content
        article_soup = bs(article_content, "html.parser")
    
        article_time = article_soup.find("time", {"itemprop": "datePublished"})
        if article_time is not None:
            article_time_str:str = article_time['datetime']
            publication_datetime = datetime.strptime(article_time_str, '%Y-%m-%dT%H:%M:%SZ')
            
            # Extract time, hour, and minutes
            publication_date: str = publication_datetime.strftime('%Y-%m-%d')
            article_date = datetime.strptime(publication_date, '%Y-%m-%d')
            published_time = publication_datetime.strftime('%H:%M:%S')
            hour = publication_datetime.hour
            minute = publication_datetime.minute

            published_time = time(hour=hour, minute=minute)
            startTime = time(hour=0, minute=0)
            endTime = time(hour=10, minute=0)


        article_category = article_soup.find("span", {"class": "c-article__category"})
        if article_category is not None:
            category = article_category.text.strip()

            if article_date.date() == today:
                if str(category) == "Göteborg" or str(category) == "Världen" or str(category) == "Sverige":
                    if datetime.combine(datetime.min, startTime) <= datetime.combine(datetime.min, published_time) <= datetime.combine(datetime.min, endTime):
                        #print(f"Date: {publication_date} and Category: {category}, Time: {published_time}")
                        article_title = article_soup.find("h1", {"class": "c-article__heading"})
                        link = shorten_url(article_url)
                        summary = f"Tid: {published_time}, {article_title.text.strip()} \nLÄNK: {link}"
                        missed_news.append(summary)
                        continue
    
    
    print("Finished reading everything...")
    picoNotify = piNotifier(missed_news)
    
def shorten_url(article_url: str) -> str:
    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(article_url)
    print(short_url)
    return str(short_url)

if __name__ == "__main__":
    url = "https://www.gp.se"
    webscrape_news(url)

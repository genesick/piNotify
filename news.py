import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta, time
from urllib.parse import urljoin


def webscrape_news(url):
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)
    
    
    # Send a GET request to the URL and get the page content
    response = requests.get(url)
    content = response.content

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
            article_time_str = article_time['datetime']
            publication_datetime = datetime.strptime(article_time_str, '%Y-%m-%dT%H:%M:%SZ')
            
            # Extract time, hour, and minutes
            publication_date = publication_datetime.strftime('%Y-%m-%d')
            published_time = publication_datetime.strftime('%H:%M:%S')
            hour = publication_datetime.hour
            minute = publication_datetime.minute

            published_time = time(hour=hour, minute=minute)
            startTime = time(hour=0, minute=0)
            endTime = time(hour=10, minute=0)

        else:
            pass
        
        article_category = article_soup.find("span", {"class": "c-article__category"})
        #print(f"Article category: {article_category}")
        if str(article_category) == "Göteborg" or str(article_category) == "Världen" and str(publication_date) == str(yesterday):
            if datetime.combine(datetime.min, startTime) <= datetime.combine(datetime.min, published_time) <= datetime.combine(datetime.min, endTime):
                article_title = article_soup.find("h1", {"class": "c-article__heading"})
                print(f"{article_title.text.strip()}")
                continue
            
    print("Finished reading everything...")

if __name__ == "__main__":
    url = "https://www.gp.se"
    webscrape_news(url)

#webscraping
import requests
from bs4 import BeautifulSoup as bs   
    
def webscrape_news():
    # URL of the website to scrape
    url = "https://www.gp.se"

    # Send a GET request to the URL and get the page content
    response = requests.get(url)
    content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = bs(content, "html.parser")

    # Find all the article links on the page
    article_links = soup.find_all("a", {"class": "sc-gPEVay bphqvL"})

    # Loop through the article links and print the article titles and URLs
    for link in article_links:
        article_url = link.get("href")
        article_title = link.get_text()
        print(article_title)
        print(article_url)
        
if "__name__" == "__main__":
    webscrape_news() 
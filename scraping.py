import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_article_info(url):
    """
    Extracts information about a single article given its URL.
    Returns a dictionary containing the title, summary, publication date, and publication time of the article.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    article_title = soup.find('h1', class_='c-article__headline').get_text().strip()
    article_summary = soup.find('div', class_='c-article__standfirst').get_text().strip()
    article_datetime = soup.find('time', itemprop='datePublished').get('datetime')
    publication_datetime = datetime.fromisoformat(article_datetime[:-1])
    article_date = publication_datetime.date()
    article_time = publication_datetime.time()
    
    return {
        'title': article_title,
        'summary': article_summary,
        'date': article_date,
        'time': article_time
    }
    
    
def get_latest_news():
    """
    Scrapes the latest news articles from gp.se that were published between midnight and 10:00 am.
    Prints the title and summary of each qualifying article.
    """
    page = requests.get('https://www.gp.se/')
    soup = BeautifulSoup(page.content, 'html.parser')
    
    article_links = soup.find_all('a', class_='c-teaser__link', href=True)
    qualifying_articles = []
    
    for link in article_links:
        url = 'https://www.gp.se' + link['href']
        article_datetime = get_article_info(url)['time']
        
        if article_datetime < datetime.strptime('10:00', '%H:%M').time() and article_datetime >= datetime.strptime('00:00', '%H:%M').time():
            qualifying_articles.append(url)
    
    for url in qualifying_articles:
        article_info = get_article_info(url)
        print(article_info['title'])
        print(article_info['summary'])
        print()

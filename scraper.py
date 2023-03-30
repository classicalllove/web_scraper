import requests
from bs4 import BeautifulSoup
import string
import os

number_of_pages = int(input())
list_of_numbers = list(range(1, number_of_pages + 1))
type_of_articles = input()

url_prefix = 'https://www.nature.com'

links = []
contents = []
headers = []
articles_list = []

for a in list_of_numbers:
    url = f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={a}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    articles_soup_ = soup.find_all('span', {'class': 'c-meta__type'}, text=f'{type_of_articles}')
    
    for link in articles_soup_:
        link_ = link.find_parent('article').find('a')
        article_link_suffix = link_.get('href')
        article_link = url_prefix + article_link_suffix
        links.append(article_link)

    for i in links:
        r = requests.get(i).content
        soup = BeautifulSoup(r, 'html.parser')
        article_header = soup.find('h1', {"class": "c-article-magazine-title"}).text
        article_header = article_header.translate(str.maketrans('', '', string.punctuation)) + '.txt'
        headers.append(article_header.replace(' ', '_'))
        article_teaser = soup.find('p', {"class": "article__teaser"}).text
        contents.append(article_teaser)

    if not os.path.exists(f"Page_{a}"):
        os.mkdir(f"Page_{a}")

    for index, file in enumerate(headers):
        text = contents[index]
        article_file = open(f"Page_{a}/{file}", 'w')
        article_file.write(text)
        article_file.close()

print('Saved all articles.')

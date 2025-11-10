import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "http://books.toscrape.com/catalogue/"
URL = BASE_URL + "category/books_1/index.html"

books = []

while True:
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text.replace('£','')
        rating = book.p['class'][1]
        books.append({"Title": title, "Price": float(price), "Rating": rating})

    next_page = soup.find('li', class_='next')
    if next_page:
        URL = BASE_URL + "category/books_1/" + next_page.a['href']
    else:
        break

df = pd.DataFrame(books)
df.to_csv("books.csv", index=False)
print("Scraping completed! Data saved to books.csv")


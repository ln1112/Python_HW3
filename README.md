# Python_HW3

Цель:
Модуль для сбора информации о книгах с сайта 

Инструкция:
Для сбора информации о книге:

book_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
result = get_book_data(book_url)

Для сбора информации о всех книгах:
result = scrape_books('https://books.toscrape.com/catalogue', is_save=True)

Для использования, необходимо иметь следующие модули:

import time
import requests
from bs4 import BeautifulSoup
import re

import time
import requests
from bs4 import BeautifulSoup
import re

def get_book_data(book_url: str) -> dict:
   """Собирает информацию книге.

    :param book_url: url книги
    :type book_url: str
    :return: Словарь, заполненый доступными данными о книге (если что-то не удалось считать, в выводе это включено не будет)
    :rtype: dict

    """

   # НАЧАЛО ВАШЕГО РЕШЕНИЯ
   response = requests.get(book_url)
   response.raise_for_status()
   html_doc = response.content
   soup = BeautifulSoup(html_doc, 'html.parser')
   soup.prettify()
   book_data = {}
   product_main_data = soup.find('div', class_='product_main')
   book_name = product_main_data.find('h1').get_text()
   book_price = product_main_data.find('p', class_='price_color').get_text()
   book_data['name'] = book_name
   book_data['price'] = book_price

   book_available_tag = product_main_data.find('p', attrs ={'class':['instock', 'availability']})
   if book_available_tag.find('i', class_ = 'icon-ok') != None:
      available_text = book_available_tag.get_text().strip('\n ')
      parsed_available_books_number = int(re.search(r'.+\((\d+) available\)', available_text).group(1))
      book_data['available'] = parsed_available_books_number
   else:
      book_data['available'] = 0

   book_rating_item_rating_classes = product_main_data.find('p', attrs = {'class': 'star-rating'}).attrs.get('class')
   book_rating = None
   for _class in book_rating_item_rating_classes:
      if _class == 'One':
         book_rating = 1
         break
      if _class == 'Two':
         book_rating = 2
         break
      if _class == 'Three':
         book_rating = 3
         break
      if _class == 'Four':
         book_rating = 4
      if _class == 'Five':
         book_rating = 5
         break

   if book_rating is not None:
      book_data['rating'] = book_rating
      
   try:
      product_description = soup.find('div', attrs = {'id':'product_description'}).find_next('p').get_text()
      book_data['product_description'] = product_description
   except:
      pass
      #ignore

   product_additional_data_table_items = (soup.find('article', class_ = 'product_page')
                                       .find('table', attrs = {'class': ['table','table-striped']}))

   for item in product_additional_data_table_items:
      if item == '\n':
         continue
      name = item.find('th').get_text()
      value = item.find('td').get_text()
      book_data['additional_parameter_'+ name] = value

   return book_data
      
def scrape_books(catalog_url, is_save=False):
   
   """Собирает информацию о книгах в каталоге.

   :param catalog_url: url каталога книг
   :type catalog_url: str
   :param is_save: сохранить вывод в файл
   :type is_save: bool
   :return: Лист словарей, заполненых данными о книгах
   :rtype: list

   """

   # НАЧАЛО ВАШЕГО РЕШЕНИЯ
   books_catalog_url = catalog_url
   result = []
   page_number = 1
   while(True):
      books_pages_url = books_catalog_url + '/category/books_1' + ('/page-'+ str(page_number) if page_number > 1 else '/index') + '.html'
      response = requests.get(books_pages_url)
      if response.status_code == 404:
         break

      response.raise_for_status()
      html_doc = response.content
      soup = BeautifulSoup(html_doc, 'html.parser')
      all_books_on_page = soup.find_all('article', class_ = 'product_pod')

      books_href = []
      for book_item in all_books_on_page:
         href_to_book_page = book_item.find('div', class_ = 'image_container').find('a')
         if href_to_book_page.has_attr('href') and len(href_to_book_page.attrs.get('href')) > 0:
               href = href_to_book_page.attrs.get('href')
               href = href.split('..')[-1]
               books_href.append(books_catalog_url + href)
      
      for url in books_href:
         book_data = get_book_data(url)
         result.append(book_data)
      
      page_number = page_number + 1
   
   if is_save:
      with open('books_data.txt', 'w') as file:
         for book_info in result:
               file.write(str(book_info)+'\n')

   return result

# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
from avitotel import Bot


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]

    return int(total_pages)

def read_csv():
    with open('avito.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)

def write_csv(data):
    with open('avito.csv', 'a', encoding='utf8') as f:
        order = ['title','price','location','number','info_seller','name','info','url']
        writer = csv.DictWriter(f, fieldnames=order)

        writer.writerow(data)

def read_csv():
    with open('avito.csv', encoding='utf8') as file:
        fieldnames = ['title', 'price', 'location', 'number', 'info_seller', 'name', 'info', 'url']
        reader = csv.DictReader(file, fieldnames=fieldnames)
        for row in reader:
            return row


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='js-catalog_serp').find_all('div',class_=
    'snippet-horizontal item item_table clearfix js-catalog-item-enum item-with-contact js-item-extended')
    for ad in ads:
        # title, price, url, location , name, info
        title = ad.find('h3', class_='snippet-title').text.strip().lower()
        # if 'манипулятор' in name:
        #     try:
        #         title = ad.find('div', class_='description').find('h3').text.strip()
        #     except:
        #         title = ''

        try:
            url = 'https://www.avito.ru' + ad.find('a', class_='snippet-link').get('href')
        except:
            url = ''

        try:
            price = ad.find('div', class_='about').text.strip()
        except:
            price = ''

        try:
            location = ad.find('div', class_='item-address').text.strip()
        except:
            location = ''

        try:
            soupurl = BeautifulSoup(get_html(url), 'lxml')
            info = soupurl.find('div', class_='item-description-text').text.strip()
        except:
            info = ''
        try:
            info_seller = soupurl.find('div', class_='seller-info-col').text.strip()
        except:
            info_seller = ''

        try:
            name = soupurl.find('div', class_='seller-info-value').text.strip()
        except:
            name = ''

        b = Bot(url)
        number = b.tel_recon()

        print(number)

        data = {'title': title,
                'price': price,
                'url': url,
                'location': location,
                'info_seller': info_seller,
                'number': number,
                'info': info,
                'name': name}
        write_csv(data)
    # else:
    #     continue


def main():
    url = 'https://www.avito.ru/novosibirskaya_oblast/remont_i_stroitelstvo'
    base_url = 'https://www.avito.ru/novosibirskaya_oblast/remont_i_stroitelstvo?'
    page_part = 'p='
    # query_part = '&q=манипулятор'

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i)  # + query_part
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()

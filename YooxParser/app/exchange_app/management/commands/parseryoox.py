import requests
from bs4 import BeautifulSoup as bs
from time import sleep
from django.core.management.base import BaseCommand
from exchange_app.models import Product
import sqlite3 # для записи в отдельную БД sqlite (метод №1)
import json # для записи в json файл (метод №2)
import csv # для записи в документ csv (метод №3)

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36', 'accept': '*/*'} # идентификационная строка клиентского приложения
HOST = 'https://www.yoox.com' # для формирования полной ссылки
FILE = 'clothes.csv' # для записи csv (метода №1)


def get_html(url, params=None): # проверка статус-кода ресурса
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html): # получение нумерации страниц
    soup = bs(html, 'html.parser')
    try:
        pagination = soup.find('li', attrs={'class': 'next-page'}).find_previous_sibling().text.strip()
        return int(pagination)
    except AttributeError:
        pagination = 1 # Если вещей только на 1 страницу
        return int(pagination)

def get_content(html): # получение контента
    soup = bs(html, 'html.parser')
    divs = soup.find_all('div', attrs={'class': 'col-8-24'}) # карточка товара
    clothes = []

    for div in divs:
        brand = div.find('div', attrs={'class': 'brand font-bold text-uppercase'}) # бренд
        if brand == None:
            continue
        group = div.find('div', attrs={'class': 'microcategory font-sans'}) # группа товара
        old_price = div.find('span', attrs={'class': 'oldprice text-linethrough text-light'}) # цена до скидки
        discount = div.find('span', attrs={'class': 'element'}) # скидка
        new_price = div.find('div', attrs={'class': 'retail-newprice font-bold'}) # цена со скидкой
        fullprice = div.find('span', attrs={'class': 'fullprice font-bold'}) # полная цена (если на товар нет скидки)
        sizes = div.find_all('span', attrs={'class': 'aSize'}) # размер
        colors = div.find_all('span', attrs={'class': 'color-circle'}) # цвет
        try:
            art = div.find('div', attrs={'class': 'itemContainer'}).get('data-current-cod10') # артикул
        except AttributeError:
            art = None

        if brand: #получение текста с наименованием бренда
            brand = brand.get_text(strip=True) if brand else None
            if brand == None:
                break

        if group: #получение текста с наименованием группы товара
            group = group.get_text(strip=True) if group else None

        try: #получение ссылки на товар
            link = div.find('div', attrs={'class': 'itemData text-center'}).find('a', attrs={'class': 'itemlink'}).get('href')
        except AttributeError:
            link = None

        if old_price: #получение числового значения с ценой товара до скидки
            old_price = old_price.get_text(strip=True).replace(' ', '').replace('руб', '') if old_price else None

        if discount: #получение размера скидки в %
            discount = discount.get_text(strip=True) if discount else None

        if new_price: #получение числового значения с ценой товара после скидки
            new_price = new_price.get_text(strip=True).replace(' ', '').replace('руб', '') if new_price else None

        if fullprice: #получение числового значения полной цены товара
            fullprice = fullprice.get_text(strip=True).replace(' ', '').replace('руб', '') if fullprice else None

        if sizes: #получение списка с размерами товара
            sizes = [size.get_text() for size in sizes]
            sizes = " ".join(sizes)
        else:
            sizes = None

        if link:  # получение текста с наименованием группы товара
            link = link if link else ''

        if colors: #получение списка с цветами товара

            colorsbox = ['Violet', 'Powder', 'Light purple', 'Gray orange', 'Sage green', 'Apricot', 'Emerald green',
                         'Yellow brown', 'Dark brown', 'Slate blue', 'Pink', 'Brown', 'Light green', 'Pastel pink',
                         'Sand', 'Purple', 'White ', 'Black', 'Light pink', 'Ocher', 'Blue gray', 'Sea wave',
                         'Yellow', 'Azure', 'Eggplant', 'Fuchsia', 'Camel', 'Red brown', 'Coral', 'Khaki', 'Blue',
                         'Steel gray', 'Orange', 'Red', 'Rusty brown', 'Green', 'Sky blue', 'Acid green', 'Turquoise',
                         'Light gray', 'Dark green', 'Dark red ', 'Ivory', 'Pastel blue ', 'Bright blue', 'Beige',
                         'Salmon pink', 'Slate blue', 'Green military', 'Grey', 'Lead gray', 'Dark blue',
                         'Light yellow', 'Lilac', 'Red brown'] # наименования цветов

            colors16 = ['693883', 'E1D3C7', 'DB8AC3', 'B1A699', '85B09A', 'ED8701', '599789', '8E7562', '7A485E',
                        '3D254A', 'E5A2B5', '836D5C', 'C0D0B0', 'BC8480', 'D2CDC1', '695755', 'FFFFFF', '000000',
                        'E8D4D7', 'CAA24F', 'A9A5A0', '1B515A', 'EBD832', '4872BA', '533345', 'B92A74', 'BEA58F',
                        '71595F', 'ED5656', 'BDB498', '214377', '55595D', 'DF4E29', 'A40000', 'AF4E2E', '3C941F',
                        'BAD5D8', 'A7CA00', '0D81A8', 'C3C9D1', '31574C', '906058', 'ECEACC', '889AAF', '373277',
                        'CDBD9A', 'E99A63', '5F789B', '5A5C35', '8B949C', '79756c', '3A476D', 'ffff81', 'AC9ECD',
                        'A0525B'] # шестнадцатеричный код цвета

            colors = [color for color in colors]
            colors = str(colors).replace('<span class="color-circle" style="background-color: #','').replace('"></span>', '').replace(' ', '').replace('[', '').replace(']', '').split(',')
        else:
            colors = 'One color'
        textcolors = []
        for i in colors:
            if i == 'O':
                textcolors.append('One color')
                break
            if i in colors16:
                index = colors16.index(i)
                text = colorsbox[index]
                textcolors.append(text)
            else:
                textcolors.append(i)

        textcolors = " ".join(textcolors)

        if art: # получение артикула товара
            art = art if art else None

        #clothes.append((brand, group, old_price, discount,new_price,fullprice,sizes,textcolors, HOST + str(link), art)) # подключается для метода №1
        #newlist_clothes = list(clothes)

        Product(
                brand = brand,
                group = group,
                old_price = old_price,
                discount = discount,
                new_price = new_price,
                fullprice = fullprice,
                sizes = sizes,
                colors = textcolors,
                link = HOST + str(link),
                art = art,
        ).save()
        print(f'product {art}')

        clothes.append({
            'brand': brand,
            'group': group,
            'old_price': old_price,
            'discount': discount,
            'new_price': new_price,
            'fullprice': fullprice,
            'sizes': sizes,
            'colors': textcolors,
            'link': HOST + str(link),
            'art': art
        })  # добавление всех полученных данных в list(dict) clothes

    return clothes

def parse(URL):
    html = get_html(URL)
    if html.status_code == 200: # проверка статус-кода ресурса
        pages_count = get_pages_count(html.text)
        clothes = []
        for page in range(1, pages_count + 1):
            print(f'Parsing page {page} of {pages_count}...')
            html = get_html(URL, params={'page': page})
            sleep(5) # пауза 5 секунда
            try:
                clothes.extend(get_content(html.text))
            except TypeError:
                break
        #save_info(clothes, FILE) #для записи csv (метод №2)
    else:
        print('URL Error')


parse('https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%BC%D1%83%D0%B6%D1%87%D0%B8%D0%BD/shoponline/balenciaga_md#/Md=221&dept=men&gender=U&season=E&suggestion=true')
parse('https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%BC%D1%83%D0%B6%D1%87%D0%B8%D0%BD/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C/shoponline/maison%20margiela_d#/d=50&dept=shoesmen&gender=U')
parse('https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%BC%D1%83%D0%B6%D1%87%D0%B8%D0%BD/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/shoponline/gucci_d#/d=42&dept=clothingmen&gender=U')
parse('https://www.yoox.com/ru/%d0%b4%d0%bb%d1%8f%20%d0%bc%d1%83%d0%b6%d1%87%d0%b8%d0%bd/shoponline?dept=mmrc_18clvnklnjns&page=1')
parse('https://www.yoox.com/ru/%D0%B4%D0%BB%D1%8F%20%D0%BC%D1%83%D0%B6%D1%87%D0%B8%D0%BD/shoponline/msgm_md#/Md=13732&d=13732&dept=men&gender=U&page=1&attributes=%7b%27ctgr%27%3a%5b%27mglr%27%5d%7d&season=X')
# тестовые прогоны парсера (общее количество вещей +- 2 тысячи)

class Command(BaseCommand):
    help = 'Parser YOOX'

    def handle(self, *args, **options):
        return


    # conn = sqlite3.connect("clothes.db")
    # cursor = conn.cursor()
    # cursor.executemany('INSERT INTO clothes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', newlist_clothes) # для занесения в базу используется новый список, а не словарь
    # conn.commit()
    # conn.close() # добавление данных в таблицу SQLite (метод №1 SQL)

    # jsonString = json.dumps(clothes, sort_keys=False, indent=4, ensure_ascii=False)
    # jsonFile = open("clothes.json", "w")
    # jsonFile.write(jsonString)
    # jsonFile.close()  # добавление всех полученных данных из переменной clothes в файл clothes.json (Метод №2)

    # def save_info(clothes, database): # функция для записи данных из переменной clothes в файл csv (Метод №3)
    #     with open(database, 'w', newline='', encoding='utf-8') as file:
    #         writer = csv.writer(file, delimiter=';')
    #         writer.writerow(['Бренд', 'Категория товара', 'Цена до скидки', 'Скидка', 'Цена со скидкой', 'Полная цена', 'Размер', 'Цвет', 'Ссылка на товар', 'Артикул'])
    #         for cloth in clothes:
    #             writer.writerow([cloth['brand'],cloth['group'],cloth['old_price'],cloth['discount'],cloth['new_price'],cloth['fullprice'],cloth['sizes'],cloth['colors'],cloth['link'], cloth['art']])






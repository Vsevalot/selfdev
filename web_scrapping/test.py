import requests
from bs4 import BeautifulSoup


def print_lime(url: str) -> None:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    product = BeautifulSoup(response.content, "html.parser").find("div", class_="product")
    product_name = product.find("h1", class_="product__title").get_text().strip()
    # print(product_name)

    print(product)


def print_hm(url: str) -> None:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    inner = BeautifulSoup(response.content, "html.parser").find("div", class_="inner")
    product_name = inner.find("h1", class_="primary product-item-headline").get_text().strip()
    # print(product_name)

    price_parbase = inner.find("div", class_="price parbase")
    print(price_parbase.prettify())


if __name__ == '__main__':
    # url = "https://www2.hm.com/ru_ru/productpage.0935470002.html"
    # print_hm(url)
    # url = "https://www2.hm.com/ru_ru/productpage.0937715001.html"
    # print_hm(url)
    url = "https://lime-shop.ru/product/5609_585-svetlo_bezhevyy"
    print_lime(url)
    url = "https://lime-shop.ru/product/112_3779_045-chernyy"
    print_lime(url)

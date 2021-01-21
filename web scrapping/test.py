import requests
from bs4 import BeautifulSoup
from typing import List

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


def get_time_to_bus(url: str, bnumber: str = "76") -> int:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    bus_list = BeautifulSoup(response.content, "html.parser").find("ul",
                                                                   class_="masstransit-brief-schedule-view__vehicles")
    buses: List[BeautifulSoup] = bus_list.find_all("li", class_="masstransit-vehicle-snippet-view _clickable")
    for bus in buses:
        bus_number = bus.find('a', class_="masstransit-vehicle-snippet-view__name").get_text().strip()
        if bus_number == bnumber:
            time_to_station = bus.find("span", class_="masstransit-prognoses-view__title-text").get_text().strip()
            if "каждые" in time_to_station:
                return -1
            else:
                minutes = time_to_station.split(' ')[0]
                return int(minutes)


if __name__ == '__main__':
    # url = "https://www2.hm.com/ru_ru/productpage.0935470002.html"
    # print_hm(url)
    # url = "https://www2.hm.com/ru_ru/productpage.0937715001.html"
    # print_hm(url)
    # url = "https://lime-shop.ru/product/5609_585-svetlo_bezhevyy"
    # print_lime(url)
    # url = "https://lime-shop.ru/product/112_3779_045-chernyy"
    # print_lime(url)

    station_url = "https://yandex.ru/maps/54/yekaterinburg/stops/stop__9811240"
    get_time_to_bus(station_url)

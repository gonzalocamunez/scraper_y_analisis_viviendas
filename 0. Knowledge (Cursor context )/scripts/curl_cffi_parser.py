# from curl_cffi import requests as curl  # curl_cffi (librería externa)
from selectolax.parser import HTMLParser
from dataclasses import dataclass
from urllib.parse import urljoin
from rich import print

@dataclass
class Anuncio:
    precio: str
    m2: str
    habitaciones: str
    piso__ext_int_ascensor: str
    detalles: List[str]
    caracteristicas_basicas: List[str]
    edificio: List[str]
    equipamiento: List[str]
    certificado_energetico: List[str]

@dataclass
class Response:
    body_html: HTMLParser
    next_page: dict


def get_page(client, url):
    # Usamos impersonation; no pasamos headers para mantener el fingerprint original
    # resp = client.get(url, impersonate="chrome120")  # MÉTODO curl_cffi.requests.Session.get (impersonation)
    # html = HTMLParser(resp.text)  # resp.text es una propiedad del objeto Response de curl_cffi
    if html.css_first("a[data-id=pagination-test-link-next]"):
        next_page = html.css_first("a[data-id=pagination-test-link-next]").attributes
    else:
        next_page = {"href": False}
    return Response(body_html=html, next_page=next_page)


def extract_text(html, selector, index):
    try:
        return html.css(selector)[index].text(strip=True)
    except IndexError:
        return "none"


def parse_detail(html):
    new_product = Anuncio(
        name=extract_text(html, "h1#product-page-title", 0),
        sku=extract_text(html, "span.item-number", 0),
        price=extract_text(html, "span.price-value", 0),
        rating=extract_text(html, "span.cdr-rating__number_13-3-1", 0),
    )
    print(new_product)


def detail_page_loop(client, page):
    base_url = "https://www.rei.com/"
    product_links = parse_links(page.body_html)
    for link in product_links:
        detail_page = get_page(client, urljoin(base_url, link))
        parse_detail(detail_page.body_html)


def parse_links(html):
    links = html.css("div#search-results > ul li > a")
    return [link.attrs["href"] for link in links]


def pagination_loop(client):
    url = "https://www.rei.com/c/backpacks"
    while True:
        page = get_page(client, url)
        detail_page_loop(client, page)
        if page.next_page["href"] is False:
            # client.close()  # MÉTODO Session.close (curl_cffi)
            break
        else:
            url = urljoin(url, page.next_page["href"])
            print(url)


def main():
    # client = curl.Session()  # CLASE curl_cffi.requests.Session
    pagination_loop(client)


if __name__ == "__main__":
    main()

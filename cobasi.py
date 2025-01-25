from playwright.sync_api import sync_playwright, Playwright
import time
from rich import print
import re

def run(playwright: Playwright):
    
    base_url = "https://www.cobasi.com.br"
    url = base_url + "/c/cachorro"
    chrome = playwright.chromium
    browser = chrome.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    time.sleep(2)
    categories = page.locator("div.subtitle-lg").all()
    products = []
    
    # Entra nas categorias de produto para o tipo de animal selecionado
    for cat in categories:
        cat.click()
        time.sleep(1)
        prods = page.locator("a").element_handles()
        
        # Identifica os produtos exibidos na listagem
        prods = list(set([p.get_attribute("href") for p in prods if "sku" in p.get_attribute("href")]))
        for prod in prods[:5]:
            prod_desc = {}
            page.goto(base_url+prod)
            page.wait_for_load_state()
            if page.is_visible("span.chip-label"):
                print("Detected more than one variation of the product.")

            prod_desc['title'] = page.locator("h1.heading-sm").text_content()
            
            for i, price in enumerate(page.locator("span.card-price").all()):
                prod_desc['price_'+str(i+1)] = price.text_content()
            prod_desc['sku'] = prod.split("sku=")[-1]
            prod_desc['ean'] = re.search("[0-9]+(?=\\/)", page.url).group()
            prod_desc['source_url'] = page.url
            technicalities_label = page.locator("th.subtitle-md").all()
            # technicalities_value = page.locator("span.body-text-md").all()
            
            for value in enumerate(technicalities_label):
                # print(technicalities_label)
                print(technicalities_label[i].text_content(), value)

            products.append(prod_desc)
            time.sleep(0.5)
        print(products)
        break

with sync_playwright() as playwright:
    run(playwright)
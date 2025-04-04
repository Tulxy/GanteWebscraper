import pandas as pd
import requests
from bs4 import BeautifulSoup
import time



# Čtení URL ze souboru Excel
def read_urls_from_excel(file_path: str) -> list:
    try:
        read = pd.read_excel(file_path)
        urls_read = read["URL"].dropna().tolist()
        return urls_read
    except Exception as e:
        print(f"⚠️ Chyba při načítání URL ze souboru: {e}")
        return []



# Cesta k Excel souboru
excel_file = "OdkazyPython.xlsx"
urls = read_urls_from_excel(excel_file)



# Třídy pro hledání cen
no_VAT_class_names = [
    'css-1x63aam ecrn3fv1', 'PriceWithoutTax', 'com-price-product-eshop__price--detail'
]

VAT_class_names = [
    'css-u07su5 ecrn3fv0', 'PriceWithTax', 'com-price-product-eshop__price-vat--detail com-price-product-eshop__price-vat--highlight'
]


# Výsledky
product_prices = []


# Scrapování
for url in urls:
    print(f"🔍 Scraping {url}...")
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        product_info = {"URL": url, "Cena bez DPH": "", "Cena s DPH": ""}

        for class_name in no_VAT_class_names:
            element = soup.find('div', class_=class_name)
            if element:
                product_info["Cena bez DPH"] = element.text.strip()
                break

        for class_name in VAT_class_names:
            element = soup.find('div', class_=class_name)
            if element:
                product_info["Cena s DPH"] = element.text.strip()
                break

        product_prices.append(product_info)
        time.sleep(1)

    except Exception as e:
        print(f"⚠️ Chyba při zpracování {url}: {e}")

# Uložení do Excelu
df = pd.DataFrame(product_prices, columns=["URL", "Cena bez DPH", "Cena s DPH"])
df.to_excel("CenyPython.xlsx", index=True)
print("✅ Data saved successfully!")

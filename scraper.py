import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
from thefuzz import fuzz
from thefuzz import process
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
class UniversalScraper:
    def __init__(self) -> None:
        pass
    def crawl(self, driver: webdriver.Chrome): 
        elements = driver.find_elements(By.CSS_SELECTOR, 'h1')
        for el in elements:
            print(el.text)
        pass

def fuzz_test(): 
    inp = input('Enter query: ')
    inp2 = input('Enter desired result: ')
    print(f"Fuzzy search evaluation: {inp} & {inp2} => partial_ratio: {fuzz.partial_ratio(inp, inp2)} | ratio: {fuzz.ratio(inp, inp2)} | token_sort_ratio: {fuzz.token_sort_ratio(inp, inp2)} | token_set_ratio: {fuzz.token_set_ratio(inp, inp2)} | WRatio: {fuzz.WRatio(inp, inp2)} | QRatio: {fuzz.QRatio(inp, inp2)} | UWRatio: {fuzz.UWRatio(inp, inp2)} | UQRatio: {fuzz.UQRatio(inp, inp2)}")


class ShopeeScraper:
    def __init__(self) -> None:
        pass
    def crawl(self, query):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            fix_hairline=True,
        )
        driver.get('https://www.temu.com/')
        driver.maximize_window()
        driver.save_screenshot('web.png')
        pass

class GoogleScraper:
    def __init__(self, file_path=None) -> None:
        self.file_path = file_path if file_path else 'danh_sach_san_pham.xlsx'
        self.df = pd.read_excel(self.file_path)
        print(self.df)
    def crawl(self):
        uCrawler = UniversalScraper()
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome()
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        for index, row in self.df.iterrows():
            products = []
            query = row['Tên MH']
            driver.get(f'https://www.google.com/search?q={query}')
            time.sleep(5)
            shopEle = driver.find_elements(By.CSS_SELECTOR, '.crJ18e > div > div > a')
            for ele in shopEle:
                if(ele.text == 'Mua sắm'):
                    ele.click()
                    break
            time.sleep(5)
            prod_names = driver.find_elements(By.CSS_SELECTOR, 'a.Lq5OHe > div > h3')
            prod_links = driver.find_elements(By.CSS_SELECTOR, 'a.Lq5OHe')
            prod_prices = driver.find_elements(By.CSS_SELECTOR, 'span.a8Pemb')
            prod_providers = driver.find_elements(By.CSS_SELECTOR, 'div.aULzUe')
            hrefs = [el.get_attribute('href') for el in prod_links]
            providers = [el.text for el in prod_providers]
            names = [prod_name.text for prod_name in prod_names]
            prices = [prod_price.text for prod_price in prod_prices]
            for name, price, href, provider in zip(names, prices, hrefs, providers):
                fuzz_ratio = fuzz.ratio(query, name)
                print(f'{name} - {price} - {provider}')

                if(price == ''):
                    continue
                if(int(price.split('₫')[0].replace('.', '')) < 1000 or price == ''):
                    continue
                product = {
                        'prod_name': name,
                        'prod_price': int(price.split('₫')[0].replace('.', '')),
                        'prod_link': href,
                        'fuzz_partial_ratio': fuzz.partial_ratio(query, name),
                        'fuzz_ratio': fuzz_ratio,
                        'provider': provider
                    }
                products.append(product)
                print(product)
                df_prods = pd.DataFrame(products)
            try:
                with pd.ExcelWriter(f'res.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
                    existing_sheets = writer.book.sheetnames
                    if query in existing_sheets:
                        existing_df = pd.read_excel(f'res.xlsx', sheet_name=query)
                        df_prods = pd.concat([existing_df, pd.DataFrame(products)], ignore_index=True)
                    df_prods.to_excel(writer, sheet_name=query, index=False)
            except FileNotFoundError:
                with pd.ExcelWriter(f'res.xlsx', mode='w', engine='openpyxl') as writer:
                    df_prods.to_excel(writer, sheet_name=query, index=False)
            
        driver.quit()
class LazadaScraper:
    def __init__(self, file_path=None) -> None:
        self.file_path = file_path if file_path else 'danh_sach_san_pham.xlsx'
        self.df = pd.read_excel(self.file_path)
        print(self.df)
    # Set up the Selenium WebDriver for Firefox
    def crawl(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f'--user-agent={UserAgent(platforms="pc").random}')
        options.page_load_strategy = 'normal'
        driver = webdriver.Chrome(options=options)
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        df_prods = pd.DataFrame(columns=['prod_name', 'prod_price', 'prod_link'])
        df_prods.to_excel(f'res.xlsx', index=False)
        driver.get(f'https://www.lazada.vn')
        for index, row in self.df.iterrows():
            products = []
            query = row['Tên MH']
            cate = row['Loại sản phẩm']
            element_search_bar = driver.find_element(By.CSS_SELECTOR, 'input.search-box__input--O34g')
            element_search_bar.send_keys(Keys.CONTROL, 'a')
            time.sleep(.5)
            element_search_bar.send_keys(query)
            time.sleep(2)
            element_search_btn = driver.find_element(By.CSS_SELECTOR, 'a.search-box__button--1oH7')
            element_search_btn.click()
            time.sleep(5)
            element_cate = driver.find_elements(By.CSS_SELECTOR, 'div.uM5g9 > div > a')
            categories = [el.text for el in element_cate]
            res = process.extract(cate, categories, scorer=fuzz.ratio)
            for el in element_cate:
                if el.text == res[0][0]:
                    el.click()
                    break
            print(res)
            time.sleep(2)
            element_prodname = driver.find_elements(By.CSS_SELECTOR, 'div.RfADt > a')
            element_price = driver.find_elements(By.CLASS_NAME, 'ooOxS')
            for name, price in zip(element_prodname, element_price):
                fuzz_ratio = fuzz.ratio(query, name.text)
                product = {
                    'prod_name': name.text,
                    'prod_price': int(price.text.split('₫')[1].replace(',', '')),
                    'prod_link': name.get_attribute('href'),
                    'fuzz_partial_ratio': fuzz.partial_ratio(query, name.text),
                    'fuzz_ratio': fuzz_ratio,
                }
                products.append(product)
            products.sort(key=lambda x: x['fuzz_ratio'], reverse=True)
            print(products)
            df_prods = pd.DataFrame(products)
            with pd.ExcelWriter(f'res.xlsx', mode='a', engine='openpyxl') as writer:
                df_prods.to_excel(writer, sheet_name=query, index=False)
        driver.quit()
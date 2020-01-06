from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import random
import sys

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path)

def scrape_info():
    browser = init_browser()

    data = []

    for i in range(1, 2):
        #url_1 = url_2 = ''
        #if i != 1:
        #    url_1 = f'{i}_p'
        #    url_2 = f'%22currentPage%22:{i}'
        
        url = "https://www.zillow.com/homes/for_rent/2-_beds/1.5-_baths/?searchQueryState={%22pagination%22:{},%22usersSearchTerm%22:%2278758%22,%22mapBounds%22:{%22west%22:-97.72983323484141,%22east%22:-97.67300105529785,%22south%22:30.385515957084774,%22north%22:30.42759397986212},%22isMapVisible%22:true,%22mapZoom%22:14,%22filterState%22:{%22beds%22:{%22min%22:2},%22baths%22:{%22min%22:1.5},%22isForSaleByAgent%22:{%22value%22:false},%22isForSaleByOwner%22:{%22value%22:false},%22isNewConstruction%22:{%22value%22:false},%22isForSaleForeclosure%22:{%22value%22:false},%22isComingSoon%22:{%22value%22:false},%22isAuction%22:{%22value%22:false},%22isPreMarketForeclosure%22:{%22value%22:false},%22isPreMarketPreForeclosure%22:{%22value%22:false},%22isForRent%22:{%22value%22:true},%22isCondo%22:{%22value%22:false},%22isApartment%22:{%22value%22:false}},%22isListVisible%22:true}"
        print("Huy 01")



        browser.visit(url1)

        print("Huy 02")

        # random sleep to avoid detection by zillow
        time.sleep(random.randrange(15, 25)) 

        print("Huy 03")

        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")
        all_cards = soup.find_all('article', class_="list-card")
        #print(all_cards)
        for card in all_cards:
            try:
                id = card['id']
                link = card.find('a', class_="list-card-link")['href']
                price = float(card.find('div', class_="list-card-price").text.replace(",","").replace("$","").replace("/mo",""))
                days = card.find('div', class_="list-card-variable-text list-card-img-overlay").text.replace(" days ago","")
                details = card.find('ul', class_="list-card-details").find_all('li')
                bed = float(details[0].text.replace(" bds",""))
                bath = float(details[1].text.replace(" ba",""))
                sqft = float(details[2].text.replace(" sqft","").replace(",",""))
                print(f'{id}, {link}, {price}, {bed}, {bath}, {sqft}') 
                data.append([id, link, price, bed, bath, sqft, days])
            except Exception as e:
                print(e)

        browser.quit()

    return data


# ================== main code ==================
print("Hello")
url1 = sys.argv[1]
print(url1)
data = scrape_info()
df = pd.DataFrame(data, columns =['code', 'link', 'price', 'bed', 'bath', 'sqft', 'days'])
df.to_csv("zillow.csv")


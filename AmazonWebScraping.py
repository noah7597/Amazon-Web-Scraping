from bs4 import BeautifulSoup
from selenium import webdriver
import csv

def get_url(search_term):
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', "+")

    # add term query to url
    url = template.format(search_term)
    
    # add page query placeholder
    #url += '&page{}'
    
    return template.format(search_term)

def extract_record(item):
    #description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    
    try:
        #price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span','a-offscreen').text
    except AttributeError:
        return
    
    try:
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except:
        rating = ''
        review_count = ''
    
    try:
        size_parent = item.find('div','a-row a-spacing-top-small s-product-specs-view')
        size = size_parent.find('span',{'class': 'a-text-bold', 'dir': 'auto'}).text
    except:
        size_parent = ''
        size = ''
    
    result = (description, price, size, rating, review_count, url)
    
    return result

def main(search_term):
    driver = webdriver.Chrome(executable_path ="/Applications/chromedriver87")
    url = 'https://www.amazon.com'
    driver.get(url)
    
    npo_products = {}
    records = []
    url = get_url(search_term)
    
    for page in range(1, 21):
        driver.get('https://www.amazon.com/s?k='+ url +'&' + 'page=' + str(page) + '&qid=1609014597&ref=sr_pg_1')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div',{'data-component-type':'s-search-result'})
        
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
        
        #url_parent = item.find('div','a-last')
        #url = 'https://www.amazon.com' + url_parent.get('href')
    
    driver.close()
    
    with open('/Users/noahhallberg/Desktop/WebScraping/amazon_product.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Size', 'Rating', 'ReviewCount', 'Url'])
        writer.writerows(records)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
from bs4 import BeautifulSoup
import requests
import pprint
import re

# constants:
url = "https://appbrewery.github.io/Zillow-Clone/"

# send request to the website:
response = requests.get(url)
html_doc = response.text

# parse the html:
soup = BeautifulSoup(html_doc, 'html.parser')

pprint.pprint(soup)


url_links_of_all_listings = []


# find all <a> tags, then filter those with 'href' attribute containing 'http'
for link in soup.find_all('a', href=True):
    if 'http' in link['href']:
        url_links_of_all_listings.append(link['href'])

# print the list of urls:
print("Property Links:")
pprint.pprint(url_links_of_all_listings)

# extracting the prices of properties:

cleaned_prices_list = []

# regular expression to match and clean prices
price_pattern = re.compile(r'\$\d+[\d,]*')
cleanup_pattern = re.compile(r'\+|/mo')

# find all span tags with the specified class for prices and clean them
for span in soup.find_all('span', class_='PropertyCardWrapper__StyledPriceLine'):
    price_match = price_pattern.search(span.text)
    if price_match:
        # Remove '+' and '/mo' from the matched price
        cleaned_price = cleanup_pattern.sub('', price_match.group())
        cleaned_prices_list.append(cleaned_price)

# print the list of cleaned prices
print("Cleaned Prices:")
pprint.pprint(cleaned_prices_list)

addresses_list = []


for address in soup.find_all('address', {'data-test': 'property-card-addr'}):
    # strip() is used to remove any leading/trailing whitespace characters
    addresses_list.append(address.text.strip())

print("\nAddresses:")
pprint.pprint(addresses_list)


# # find all listings on the page:
# listings = soup.find_all('div', class_='search-result-card')
#
# # initialize the result list:
# rental_properties = []
#
# # iterate over each listing:
# for listing in listings:
#     # extract price:
#     price_element = listing.find('div', class_='list-card-price')
#     price = price_element.get_text().strip() if price_element else 'N/A'
#
#     # extract address:
#     address_element = listing.find('address', class_='list-card-addr')
#     address = address_element.get_text().strip() if address_element else 'N/A'
#
#     # extract url:
#     url_element = listing.find('a', class_='list-card-link')
#     listing_url = url_element['href'] if url_element else 'N/A'
#
#     # check if the listing meets the criteria:
#     if '1+ bd' in listing.get_text() and 'up to $3K' in listing.get_text():
#         rental_properties.append({
#             'price': price,
#             'address': address,
#             'url': listing_url
#         })
#
# # print the result:
# for property in rental_properties:
#     print(f"Price: {property['price']}, Address: {property['address']}, URL: {property['url']}")


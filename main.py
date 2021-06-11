import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22ma" \
             "pBounds%22%3A%7B%22west%22%3A-122.70526523779272%2C%22east%22%3A-122.3035776157224%2C%22south%22%3A37" \
             ".65614532704804%2C%22north%22%3A37.882484971549296%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22" \
             "%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22v" \
             "alue%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22" \
             "auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22" \
             "%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%" \
             "22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atr" \
             "ue%2C%22mapZoom%22%3A12%7D"
GOOGLE_FORM = "https://forms.gle/MHMUpFhenSUnP6tL8"


def search_hrefs():
    """
       Search the HTML for links of the properties. \n
       Form these into a list.

       :return: list of URLs
    """
    link_list_soup = soup.find_all(name="a", class_="list-card-link")
    link_list = [link.get("href") for link in link_list_soup]
    # Remove duplicates
    link_list = list(dict.fromkeys(link_list))
    # Some links are broken
    # e.g. '/b/1450-castro-st-san-francisco-ca-5YVg2f/'
    # should be 'https://www.zillow.com/b/1450-castro-st-san-francisco-ca-5YVg2f/'
    for link in link_list:
        if not link.startswith("https"):
            link_list[link_list.index(link)] = 'https://www.zillow.com' + link

    return link_list


def search_adress():
    """
           Search the HTML for addresses of the properties. \n
           Form these into a list.

           :return: list of addresses
    """
    address_list_soup = soup.find_all(name="address", class_="list-card-addr")
    address_list = [address.getText() for address in address_list_soup]

    return address_list


def search_prieces():
    """
           Search the HTML for prieces of the properties. \n
           Form these into a list.

           :return: list of preices
    """
    preices_list_soup = soup.find_all(name="div", class_="list-card-price")
    preices_list = [preices.getText() for preices in preices_list_soup]

    return preices_list


def auto_fill(links, addresses, prices):
    """
               Auto fills google form with link, address and price of the found property.

               :parameter links: list of links
               :parameter addresses: list of addresses
               :parameter prices: list of prices

    """
    driver_path = "D:\__DEV__\chromedriver.exe"
    driver = webdriver.Chrome(driver_path)
    driver.maximize_window()
    driver.get(GOOGLE_FORM)

    sleep(1)
    for item in links:
        index = links.index(item)
        form_link = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        form_link.send_keys(links[index])
        form_address = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        form_address.send_keys(addresses[index])
        form_price = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        form_price.send_keys(prices[index])
        driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span').click()
        sleep(1)
        driver.find_element_by_link_text("Prześlij kolejną odpowiedź").click()
        sleep(2)


# Needed to add header due to captcha
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472."
                  "77 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
}

# Scraping Zillow for all properties in San Francisco for rent with one bedroom and up to 3000$
response = requests.get(url=ZILLOW_URL, headers=headers)
zillow_website = response.text
soup = BeautifulSoup(zillow_website, "html.parser")

links_li = search_hrefs()
addresses_li = search_adress()
prices_li = search_prieces()

auto_fill(links_li, addresses_li, prices_li)

import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import json

driver = webdriver.Chrome(service=Service(executable_path="D:\chromedriver\chromedriver.exe"))
zillow_url = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
             "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A" \
             "-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C" \
             "%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A" \
             "%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse" \
             "%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B" \
             "%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D" \
             "%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min" \
             "%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D "
google_form_url = GOOGLE_FORM_LINK

header = {
    'Accept-Language': "en-US,en;q=0.6",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 "
                  "Safari/537.36 "
}

final_data = {
    "address": [],
    "price": [],
    "link": []
}

# getting website
response = requests.get(zillow_url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")

# finding property element
all_details = soup.find("script", attrs={'type': 'application/json', 'data-zrr-shared-data-key': 'mobileSearchPageStore'}).text
json_data = all_details.strip("-->").strip("<!--")

# json file formatting
property_details = json.loads(json_data)
details = property_details["cat1"]["searchResults"]["listResults"]

for data in details:
    link = "https://www.zillow.com"
    final_data["address"].append(data["address"])
    try:
        final_data["price"].append(data['units'][0]["price"])
    except KeyError:
        final_data["price"].append(data["price"])
    if "http" not in data["detailUrl"]:
        final_data["link"].append(link + data["detailUrl"])
    else:
        final_data["link"].append(data["detailUrl"])

# fill google form
driver.get(google_form_url)

for i in range(len(final_data["price"])):
    all_input = driver.find_elements(By.CSS_SELECTOR, "[type = 'text']")
    time.sleep(1)
    all_input[0].send_keys(final_data["address"][i])
    all_input[1].send_keys(final_data["price"][i])
    all_input[2].send_keys(final_data["link"][i])
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span').click()
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '/html/body').click()
    except NoSuchElementException:
        print("no element")
    driver.find_element(By.CSS_SELECTOR, "a").click()


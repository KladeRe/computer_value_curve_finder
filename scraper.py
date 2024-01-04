import requests
from bs4 import BeautifulSoup

r = requests.get("https://taitonetti.fi/kaytetyt-kannettavat-tietokoneet?limit=160")

soup = BeautifulSoup(r.content, "html.parser")

grading = soup.find_all("div", class_="kl_tarra")

descriptions = soup.find_all("h2", class_="product-name")

prices = soup.find_all("p", class_="price")

for i in range(len(prices)):

    if prices[i].find("span", class_="price-new"):
        prices[i] = prices[i].find("span", class_="price-new").text.strip()
    else:
        prices[i] = prices[i].text.strip()

for price in prices:
    print(price)




import requests
import re
from bs4 import BeautifulSoup

r = requests.get("https://taitonetti.fi/kaytetyt-kannettavat-tietokoneet?limit=160")

soup = BeautifulSoup(r.content, "html.parser")

# Collect all data from the website

grading_divs = soup.find_all("div", class_="kl_tarra")

descriptions_divs = soup.find_all("h2", class_="product-name")

prices = soup.find_all("p", class_="price")



def returnText(s):
    return s.text

grading_translations = {
    " Erinomainen kunto": 3,
    " Hyvä kunto": 2,
    " Kohtalainen kunto": 1
}

def convertGradingToValue(s):
    return grading_translations[returnText(s)]

gradings = list(map(convertGradingToValue, grading_divs))

descriptions = list(map(returnText, descriptions_divs))

for i in range(len(prices)):

    if prices[i].find("span", class_="price-new"):
        prices[i] = prices[i].find("span", class_="price-new")

    prices[i] = float(prices[i].text.strip().replace(",", "")[:-2])


def getSpecs(txt):
    x = re.search("(i5|i3|i7|Ryzen).*", txt)
    return x.group().split("/")[:3]

specs = list(map(getSpecs, descriptions))

for spec in specs:
    spec[1] = int(spec[1])
    if "SSD" in spec[2]:
        spec[2] = spec[2][:-3]
    
    if "GB" in spec[2]:
        spec[2] = spec[2][:-2]
    
    if "TB" in spec[2]:       
        spec[2] = spec[2][:-2]+"000"
    spec[2] = int(spec[2])


# Writes data to a file

with open("PCs.csv", "w") as f:
    f.write("Grading,Processor,RAM,Storage,Price\n")

    for i in range(len(specs)):
        f.write(f"{gradings[i]},{specs[i][0]},{specs[i][1]},{specs[i][2]},{prices[i]}\n")



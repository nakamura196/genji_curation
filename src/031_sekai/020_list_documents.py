import requests
from bs4 import BeautifulSoup

url = "http://www.genji-monogatari.net/xml/eshibuya/text/text54.1.xml"

soup = BeautifulSoup(open('data/text54.1.xml'), 'xml')

print(soup)

rows2 = soup.find_all("章")

texts = []

for row2 in rows2:

    no2 = row2.get("no")    

    rows = row2.find_all("行")

    for row in rows:
        no = row.get("no")
        print(no2, no, row.text)
        texts.append("({}-{}){}".format(no2, no, row.text))

    # print(soup)

print(texts)

with open("output/54.txt", mode='w') as f:
    f.write("".join(texts))
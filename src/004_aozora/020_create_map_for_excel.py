import requests
from bs4 import BeautifulSoup
import re
from bs4 import BeautifulSoup

import requests
import openpyxl

book = openpyxl.Workbook()

soup = BeautifulSoup(open('data/xml_s/01.xml','r'), "lxml")

sheet = book.create_sheet(index=0)

sheet.append(["現代語訳ID", "現代語訳テキスト"])

# main_text.contents = all
s_arr = soup.find_all("s")
for s in s_arr:
    id = s.get("xml:id")
    text = s.get_text().replace(" ", "").replace("\n", "")

    print(id, text)
    sheet.append([id, text])

book.save('data/check/modern.xlsx')

    
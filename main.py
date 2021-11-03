from bs4.element import Tag
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# browser = webdriver.Chrome(executable_path="./drivers/chromedriver")
# browser.get('https://www.businesslist.com.ng/location/lagos/3')
index = 1
# URL = f'https://www.businesslist.com.ng/location/lagos/{index}'
BASE_URL = 'https://www.businesslist.com.ng'
web_pages = []
for i in range(40):
    index +=1
    URL = f'https://www.businesslist.com.ng/location/lagos/{index}'
    print('Going through index ', index)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    companies = (soup.find_all('h4'))
    companies_link_list = []
    for company in companies:
        companies_link_list.append(company.find('a').get('href'))


    # print(companies)
    # print(companies_link_list)

    # print(BASE_URL+companies_link_list[1])

    
    for link in companies_link_list:
        web_page = BASE_URL+link
        web_pages.append(web_page)

import xlsxwriter
from xlsxwriter import workbook

wb = xlsxwriter.Workbook("0000 Company details.xlsx")

company_dict = {}
names = []
adresses = []
numbers = []
sites = []
i = 0

for x in web_pages:
    i +=1
    print("Parsing site ", i)
    URL = x
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    company_name = (soup.find(id='company_name')).get_text()
    company_adress = (soup.find(class_= 'text location')).get_text()
    other_numbers = (soup.find(class_ = 'text')).get_text()
    print(other_numbers)
    # print(company_adress.get_text())
    # print(company_name.get_text())

    try:
        company_number = (soup.find(class_= 'text phone'))
        company_number = company_number.get_text()
    except:
        company_number = "Not Found"
    try:
        company_site = (soup.find(class_= 'text weblinks')).find_all('a')
        for links in company_site:
            company_link = (links.get('href'))
    except:
        company_link = "Not Listed"

    names.append(company_name)
    adresses.append(company_adress)
    numbers.append(company_number)
    sites.append(company_link)

worksheet = wb.add_worksheet()
row = 0
column = 0

for item in names:
    worksheet.write(row, column, item)
    row+=1
row = 0
for item in adresses:
    worksheet.write(row,1,item)
    row+=1
row = 0
for item in numbers:
    worksheet.write(row,2,item)
    row+=1
row = 0
for item in sites:
    worksheet.write(row,3,item)
    row+=1

wb.close()

print("NAMES", names)
print("ADRESSES", adresses)
print("NUMBERS", numbers)
print("SITES", sites)

print(len(names))
print(len(adresses))
print(len(numbers))
print(len(sites))

i=0
for x in numbers:
    if x == "Not Found":
        i +=1
print(i)


# time.sleep(10)
# browser.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from random import random
from bs4 import BeautifulSoup
import pandas as pd

options = webdriver.ChromeOptions() # setting options for window
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome('chromedriver', options=options) # start and get target page
driver.get("https://store.steampowered.com/stats/?l=english")

sleep(1 + random()) # delay

element = driver.find_element(By.ID, "detailLink") # find and push button to increase list of games to parse
element.click()

html = driver.page_source # now parse the full table
soup = BeautifulSoup(html, "html.parser")
table = soup.find("div", {"id" : "detailStats"}).find("tbody")
my_table = []
for index, row in enumerate(table.findAll("tr")):
    cells = row.findAll("td")
    for i in range(len(cells)):
        cells[i] = (cells[i].getText()).strip()
    new_cells = []
    for cell in cells:
        if len(cell) != 0:
            new_cells.append(cell)
    if len(new_cells) != 3:
        continue
    if (index != 0):
        for i in range(2):
            new_cells[i] = int(new_cells[i].replace(",", ""))
    my_table.append(new_cells)
pd.DataFrame(my_table[1:]).to_csv('SteamOnline.csv', index=False, header=my_table[0])

driver.quit()




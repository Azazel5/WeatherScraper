import requests
import pandas as pd 
from datetime import date
from selenium import webdriver
from bs4 import BeautifulSoup

class WeatherScraper():
    def __init__(self):
        self.driver = webdriver.Chrome() 

    def extract_data(self):
        self.driver.get('https://www.dnr.state.mn.us/climate/climate_monitor/climate_observatory.html')
        link = self.driver.find_element_by_xpath(
        '//*[@id="main_page_content"]/div[2]/article/div/div/ul[1]/li[2]/a').get_attribute('href')
        self.driver.get(link)
        self.driver.close()

        dict_list = []
        req = requests.get(link)
        soup = BeautifulSoup(req.text, 'html.parser')
        headers = soup.find_all('th')
        for row in soup.find_all('tr'):
            data = {}
            columns = row.find_all('td')
            for i in range(len(columns)):
                data[headers[i].text] = columns[i].text
            if data != {}:
                dict_list.append(data)

        df = pd.DataFrame(dict_list)
        todays_date = date.today()
        df.to_csv('data_' + str(todays_date) + '.csv')

        
        
            


 
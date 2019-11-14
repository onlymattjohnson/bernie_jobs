# Import Libraries
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import datetime
import csv
import pandas as pd

class GreenhousePage:
    def __init__(self, slug):
        self.slug = slug
        self.run_date = datetime.date.today().strftime("%Y-%b-%d")  
        self.url = 'https://boards.greenhouse.io/' + self.slug
        self.load_soup()
        self.title = self.soup.find("meta", property = "og:title")['content']
        self.sections = []
        self.get_sections()
        self.jobs_data = [['category','job_title','page_link','job_id', 'location', 'run_date']]
        self.load_jobs()
        self.load_dataframe()
    
    def load_jobs(self):
        sec_divs = self.soup.findAll("section")
        for sec in sec_divs:
            
            all_links = sec.findAll('a', attrs={'data-mapped': 'true'})
            for link in all_links:
                category = link.find_previous("h3").text
                job_title = link.contents[0]
                page_link = 'https://boards.greenhouse.io' + link['href']
                job_id = link['href'][len(self.slug + "/jobs/") + 1:]
                location = link.find_next_sibling('span').text
                self.jobs_data.append([category, job_title, page_link, job_id, location, self.run_date])
    
    def load_dataframe(self):
        self.jobs = pd.DataFrame(self.jobs_data[1:], columns = self.jobs_data[0])
            
    def get_sections(self):
        if not self.soup:
            self.load_soup()
        sec_divs = self.soup.findAll("section")
        for sec in sec_divs:
            try:
                sec_title = sec.find("h3").text
                self.sections.append(sec_title)
            except:
                pass
            
    def load_soup(self):
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        
    def print_html(self):
        print(self.soup.prettify())
    
    def to_csv(self):
        self.jobs.to_csv(self.run_date + '.csv')

bernie_page = GreenhousePage('bernie2020')
bernie_page.to_csv()
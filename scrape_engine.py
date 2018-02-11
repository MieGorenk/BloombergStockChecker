import requests
from bs4 import BeautifulSoup
import lxml
import os
import json

# this function will retrieve the urls from txt file 
# and then will return string of urls
def retrieve_urls():
  file = open("urls.txt", "a+")
  urls = file.read().split(",")
  return urls

# this function will scrape the content of the website
# and return the stock info in a dictionary
def scrape_web(url):
  site = requests.get(url)
  soup = BeautifulSoup(site.content, 'lxml')
  info = set_info_to_json(soup)

# this function will get the necesary info of the stock
def get_info(soup):
  pass

def set_info_to_json(soup):
  name = soup.find("span", class_="companyId__87e50d5a").text
  info = {name : 
          {'Name': soup.find("h1", class_ = "companyName__99a4824b").text,
          'Price' : soup.find('span', class_ = "priceText__1853e8a5").text,
          'Currency' : soup.find("span", class_ = "currency__defc7184").text,
          'Open': soup.find_all("div", class_ = "value__b93f12ea")[0].text,
          'Prev Close' : soup.find_all("div", class_ = "value__b93f12ea")[1].text,
          'Volume' : soup.find_all("div", class_ = "value__b93f12ea")[2].text,
          'Market Cap' : soup.find_all("div", class_ = "value__b93f12ea")[3].text,
          'Day Range' : soup.find_all("div", class_="text")[0].text,
          '52 Week Range' : soup.find_all("div", class_="text")[1].text
          }}
  write_json(info)

def write_json(info):
    if os.stat("data.json").st_size == 0:
      with open('data.json', 'w') as file:
        json.dump(info, file)
    else:
      data = read_json()
      data.update(info)
      with open('data.json', 'w') as file:
        json.dump(data, file)
  
def read_json():
  with open('data.json') as file:
    data = json.load(file)
  return data

def refresh_data():
  file = open('urls.txt', 'r')
  urls = file.read().split(",")
  print(urls)

  # delete the content to be refreshed
  json_data = open('data.json', 'w')
  json_data.seek(0)
  json_data.truncate()

  for i in urls:
    if i == "":
      continue
    else:
      scrape_web(i)

# this function will add url to the txt 
# and will check if the url is from bloomberg & reachable
def add_url_to_file(url):
  file = open("urls.txt", "a+")
  if("bloomberg.com" in url):
    webpage = requests.get(url)
    if(webpage.status_code == 200):
      file.write(url+",")
      scrape_web(url)
      return "VALID"
    elif url in file.read():
      return "EXIST"

  else:
      return "NOT VALID"



  




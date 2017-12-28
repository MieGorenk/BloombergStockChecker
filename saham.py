import requests
from bs4 import BeautifulSoup
import lxml
import os

def main():
    #open the file
    file = open("listWeb.txt", "a+")

    #if the file is still empty
    if(os.stat("listWeb.txt").st_size == 0):
        start_up(file)
    else: 
        read_file(open("listWeb.txt","r" ))

def start_up(file):
    jumlah_web = input("please the number of web that u want to enter? ")
    for i in range(int(jumlah_web)):
        webpage = input("enter your webpage: ")
        add_web_to_file(file, webpage)

def read_file(file):
    list_web = file.read().split(",")
    print(list_web)
    scrape(list_web)

def scrape(list_web):
    for page in list_web:
        if(page == ""):
            continue
        data = []
        site = requests.get(page)
        soup = BeautifulSoup(site.content, 'lxml')
    
        name = soup.find("span", class_="companyId__87e50d5a").text
        price = soup.find("span", class_="priceText__1853e8a5").text
        day_range = soup.find_all("div", class_="text")[0]
        day_low = soup.find("span", class_="textLeft").text
        day_high = soup.find("span", class_="textRight").text
        data.append(name)
        data.append(price)
        data.append(day_low)
        data.append(day_high)
        print_detail(data)
    
def print_detail(data):
    print("============")
    print("Name: " + data[0])
    print("Price: " + data[1])
    print("Day-Range: " + data[2] + "-" + data[3])
    print("============")


def add_web_to_file(file, webpage):
    file.write(webpage+",")



main()

# WSKT_site = requests.get("https://www.bloomberg.com/quote/WSKT:IJ")
# WSKT_soup = BeautifulSoup(WSKT_site.content,'lxml')

# #print(waskita_soup.prettify())
# WSKT_price = WSKT_soup.find("span", class_="priceText__1853e8a5").text
# WSKT_day_range = WSKT_soup.find_all("div", class_="text")[0]
# WSKT_day_low = WSKT_soup.find("span", class_="textLeft").text
# WSKT_day_high = WSKT_soup.find("span", class_="textRight").text

# print("===WSKT===")
# print("Price:" + WSKT_price)
# print("Range:" + WSKT_day_low + "-" + WSKT_day_high)
# print("==========")





#TODO make GUI App
#TODO make exceptions for user 
import requests
from bs4 import BeautifulSoup
import lxml
import os

def main():
    #open the file
    file = open("listWeb.txt", "a+")

    #check the status of the file
    if(os.stat("listWeb.txt").st_size == 0):
        start_up(file)
        read_file(open("listWeb.txt","r" ))

    else: 
        read_file(open("listWeb.txt","r" ))

#initializing the webpages on the txt file
def start_up(file):
    try:
        jumlah_web = input("please the number of web that u want to enter? ")
        for i in range(int(jumlah_web)):
            webpage = input("enter your webpage: ")
            add_web_to_file(file, webpage)
    except ValueError:
        print("Please enter an Integer!")
        start_up(file)

#read the contents of the file
def read_file(file):
    list_web = file.read().split(",")
    print(list_web)
    scrape(list_web)

#scrape the data from the webpages
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

 #print the data   
def print_detail(data):
    print("============")
    print("Name: " + data[0])
    print("Price: " + data[1])
    print("Day-Range: " + data[2] + "-" + data[3])
    print("============")

#adding file to the file
#user can add the website manually from the txt
#the site can only come from bloomberg
def add_web_to_file(file, webpage):
    file.write(webpage+",")



main()







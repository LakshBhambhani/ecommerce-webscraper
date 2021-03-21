from bs4 import BeautifulSoup
import requests
import re

# webpageurls = ['https://www.amway.com/en_US/XS™-Energy-%2B-Burn-–-Blood-Orange-p-293055', 'https://www.amsterdamprinting.com/p/premium-zippered-tote?id=48634']

webpageurls = []

def readFile(fileName):
    fileObj = open(fileName, "r") #opens the file in read mode
    words = fileObj.read().splitlines() #puts the file into an array
    fileObj.close()
    return words

webpageurls = readFile("urls.txt")

# print(webpageurls)

for url in webpageurls:
    data = requests.get(url)

    soup = BeautifulSoup(data.text,'html.parser')

    titles = []
    details = []
    descriptions = []

    description = ""

    #title
    for title in soup.findAll("h1", {"class": lambda y: y and y.find('title')}):
        titles.append(title.text)
    for title in soup.findAll("h1", {"class": lambda y: y and y.find('product_title')}):
        titles.append(title.text)
    for title in soup.findAll("h1"):
        titles.append(title.text)
    for title in soup.findAll("product-single__title"): #shopify
        titles.append(title.text)
        # print(title)

    #brief summary
    for details in soup.findAll("div", {"id": lambda y: y and y.find('details')}):
        details.append(details.text)
    
    #description
    for description in soup.findAll("div", {"id": lambda y: y and y.find('description')}):
        descriptions.append(description.text)
    for description in soup.findAll("div", {"id": lambda y: y and y.find('product-single__description')}): #shopify
        descriptions.append(description.text)
    for description in soup.findAll("div", {"id": lambda y: y and y.find('product-details__description')}): #shopify
        descriptions.append(description.text)
        
    

    max_len = -1
    for desc in descriptions:
        if len(desc) > max_len: 
            max_len = len(desc) 
            description = desc 

    #logging
    if(len(titles) > 0):
        print("Title: " + " ".join(str(titles[0]).split()))
    
    # if(len(details) > 0):
    #     print("Details: " + " ".join(str(details).split()))

    # if(len(descriptions) > 0):  
    #     print("Description: " + " ".join(str(description).split()))



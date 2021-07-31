from bs4 import BeautifulSoup
import requests
import re
import pandas
import operator
from difflib import SequenceMatcher
# import Ecommerce_Webscraper.Ecommerce_Webscraper.spiders.generic

# webpageurls = ['https://www.amway.com/en_US/XS™-Energy-%2B-Burn-–-Blood-Orange-p-293055', 'https://www.amsterdamprinting.com/p/premium-zippered-tote?id=48634']

webpageurls = []

def readFile(fileName):
    fileObj = open(fileName, "r") #opens the file in read mode
    words = fileObj.read().splitlines() #puts the file into an array
    fileObj.close()
    return words

def find_matching_key(list_in, max_key_only = True):
  """
  returns the longest matching key in the list * with the highest frequency
  """
  keys = {}
  curr_key = ''

  # If n does not exceed max_n, don't bother adding
  max_n = 0

  for word in list(set(list_in)): #get unique values to speed up
    for i in range(len(word)):
      # Look up the whole word, then one less letter, sequentially
      curr_key = word[0:len(word)-i]
      # if not in, count occurance
      if curr_key not in keys.keys() and curr_key!='':
        n = 0
        for word2 in list_in:
          if curr_key in word2:
            n+=1
        # if large n, Add to dictionary
        if n > max_n:
          max_n = n
          keys[curr_key] = n
    # Finish the word
  # Finish for loop  
  if max_key_only:
    return max(keys, key=keys.get)
  else:
    return keys    


webpageurls = readFile("newurls.txt")

# print(webpageurls)

for url in webpageurls:
    data = requests.get(url)

    originalSoup = BeautifulSoup(data.text,'html.parser')

    product_text = originalSoup.findAll('div', attrs={'itemtype': 'http://schema.org/Product'})
    soup = BeautifulSoup(str(product_text), 'html.parser')


    titles = []
    details = []
    descriptions = []
    prices = []
    schemas = []
    images = []

    description = ""

    num_images = 0

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

    #price
    for price in soup.findAll("div", {"class": lambda y: y and y.find('singlePrice')}):
        prices.append(str(price.text)[str(price.text).find('$'):str(price.text).find(' ', str(price.text).find('$'))])
    for price in soup.findAll("price"): #shopify
        prices.append(str(price.text)[str(price.text).find('$'):str(price.text).find(' ', str(price.text).find('$'))])
    for price in originalSoup.findAll('div', attrs={'itemtype': 'http://schema.org/Offer'}):
        prices.append(str(price.text)[str(price.text).find('$'):str(price.text).find(' ', str(price.text).find('$'))])

    #images
    try:
        for images in soup.findAll("div", {"class": lambda y: y and y.find('product-image')}): #shopify
            num_images+=1
        if num_images == 0 or num_images > 25:
            num_images = 0
            for image in soup.findAll('img'):
                if 'product' in str(image['src']):
                    num_images+=1
            if(num_images > 25):
                num_images = 0
                for image in soup.findAll('img'):
                    if 'product' in str(image['src']) and str(titles[0]) in str(image['alt']):
                        num_images+=1
    except:
        num_images = num_images

    #reviews
    for review in soup.findAll("span", {"role": lambda y: y and y.find('status')}, {"aria-live": lambda y: y and y.find('polite')}):
        print(soup)

    #specifications
    # for review in originalSoup.findAll("div", {"class": lambda y: y and y.find('pd_details')}):
    #     if '<div class="pd_details"' in str(review):
            # print(review)


    max_len = -1
    for desc in descriptions:
        if len(desc) > max_len: 
            max_len = len(desc) 
            description = desc 

    for schema in soup.findAll("schema"): #shopify
        schemas.append(schema.text)

    if(len(titles) == 0):
        for title in originalSoup.findAll("h1", {"class": lambda y: y and y.find('title')}):
            titles.append(title.text)
        for title in originalSoup.findAll("h1", {"class": lambda y: y and y.find('product_title')}):
            titles.append(title.text)
        for title in originalSoup.findAll("h1"):
            titles.append(title.text)
        for title in originalSoup.findAll("product-single__title"): #shopify
            titles.append(title.text)

    specs = ""
    for listitems in originalSoup.findAll('li'):
        specs += listitems.get_text()

            # specs.append(listitems.get_text())
    specs = specs.replace('\n','')

    if(':' in specs):
        for listitems in originalSoup.findAll('li'):
            if(':' in listitems.get_text()):
                specs += listitems.get_text() + '\n'


    #logging
    if(len(titles) > 0):
        print("Title: " + " ".join(str(titles[0]).split()))
        print("Specs: " + " ".join(specs))
        print("Price: " + " ".join(find_matching_key(prices, False)))
        # print("Price: " + " ".join(str(prices).split()))
        if len(str(num_images)) > 30:
            num_images = 0
        print("Num of Images: " + str(num_images))
    else:
        print('n/a')

    
    if(len(details) > 0):
        print("Details: " + " ".join(str(details).split()))

    if(len(descriptions) == 0):
        for description in originalSoup.findAll("div", {"id": lambda y: y and y.find('description')}):
            descriptions.append(description.text)
        for description in originalSoup.findAll("div", {"id": lambda y: y and y.find('product-single__description')}): #shopify
            descriptions.append(description.text)
        for description in originalSoup.findAll("div", {"id": lambda y: y and y.find('product-details__description')}): #shopify
            descriptions.append(description.text)
        max_len = -1
        for desc in descriptions:
            if len(desc) > max_len: 
                max_len = len(desc) 
                description = desc 


    if(len(description) > 0):  
        print("Description: " + " ".join(str(description).split()))



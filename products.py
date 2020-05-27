from bs4 import BeautifulSoup as soup
from pandas import DataFrame as df
import requests
import logging
from urllib.request import urlopen as uReq
import csv
import os
logging.basicConfig(filename='logs', level=logging.DEBUG)
import mysql
from mysql import connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="12345",
  database="mobile"
)
print("db connected")                    


class scraps:
    query=input('Enter search query:')
    search=query.replace(" ","%20")
    my_url = 'https://www.flipkart.com/search?q=' + search + '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    uClient = uReq(my_url)
    page_html=uClient.read()
    uClient.close()
    page_soup = soup(page_html,"lxml")
    containers = page_soup.findAll("div",{"class":"_3O0U0u"})
    
    response = requests.get(my_url)
    raw_html = response.content
    soup = soup(raw_html, 'lxml')
    klass = '_2yAnYN'

    pages1 = soup.find(class_=klass)
    pages1=pages1.text
    print(pages1)
    res = [int(i) for i in pages1.split() if i.isdigit()] 
    start=res[0]
    end=res[1]
    url1="https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="
    pages_url_list = list()   
    
    pages_url_list.append(url1)
    print(pages_url_list)
        
    with open('flipkart.csv','a',encoding='utf-8',newline='')as f_output:
        csv_print=csv.writer(f_output)
        file=os.stat('red.csv').st_size==0
        if file:
            csv_print.writerow(['product_name','rating','price'])
                
        for page in range(1, end):
            url =  url1 + str(page)
            for  container in containers:
                
            #print(container.prettify())
                product_name = container.div.img["alt"]  
                product_name=product_name.replace(","," | ")              #replacing comas cause in csv coma seperates different values
        #print("====================") 
                print( product_name )  
        #print("====================")
        
                price_container=container.findAll("div",{"class" : "_1vC4OE _2rQ-NK"})
                try:
                    price = price_container[0].text.replace("₹"," ")
                    price=price.replace(",","")
            #print("====================")                                 #replacing comas cause in csv coma seperates different values
                    print( price )
            #print("====================")
                except (IndexError, ValueError):
                    pass
        
        
                rating=container.findAll("div",{"class" : "hGSR34"})
                try:                                                    #to solve index error in certain cases
                    rating = rating[0].text        
                    rating=rating.replace(","," ")                           #replacing comas cause in csv coma seperates different values
            #print("====================")
                    print( rating)
            #print("====================")
                except (IndexError, ValueError):
                    pass
                csv_print.writerow([product_name,rating,price])    
                item1=[product_name,rating,price]
                mycursor =mydb.cursor()
                sql = "INSERT INTO flipkart (product_name,rating,price) VALUES (%s, %s,%s)"
                val=(product_name,rating,price)
                number_of_rows = mycursor.execute(sql, val)
                mydb.commit()
                print("inserted")
                
scraps()

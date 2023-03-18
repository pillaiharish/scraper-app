# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,jsonify
from bs4 import BeautifulSoup as bs
from flask_cors import cross_origin,CORS
import requests
from urllib.request import urlopen as uReq
import logging,json


logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

# app = Flask(__name__)

# @app.route("/",methods=['GET'])
# def ip_request():
#     if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
#         return(request.environ['REMOTE_ADDR'])
#     else:
#         return(request.environ['HTTP_X_FORWARDED_FOR']) # if behind a proxy

# if __name__ == "__main__":
#     app.run(debug=True,host="0.0.0.0",port=5010)


def search_url(search_keywords,website=None):
    if website == None:
        website = "www.flipkart.com"
    website_url = f"https://{website}/"
    website_url_search = website_url + "search?q=" + search_keywords
    logging.debug(website_url_search)
    url_client = uReq(website_url_search)
    url_page_source = url_client.read()
    url_client.close()
    url_html = bs(url_page_source,'html.parser')
    # logging.debug(url_html)
    big_boxes = url_html.find_all("div",{'class':'col-12-12'})
    logging.debug(len(big_boxes)) # length is 33
    # big boxes starts from 8
    # logging.debug(big_boxes[6].find_all('a', 'href'))
    first_page_sub_urls = []
    for box in url_html.find_all("div",{'class':'col-12-12'}):
        for b in box.find_all("a"):
            temp_string = b.get('href')
            if "&page=" not in temp_string and search_keywords in temp_string and ".SEARCH" in temp_string:
                first_page_sub_urls.append(temp_string)

    for i in range(len(first_page_sub_urls)):
        first_page_sub_urls[i] = "https://www.flipkart.com" + first_page_sub_urls[i]
    
    logging.debug(f"{first_page_sub_urls[9]} 9th url is the first product link")

    comments_data = dict()
    logging.debug(first_page_sub_urls)
    
    for i in range(1):
        print(i)
        request_products = requests.get(first_page_sub_urls[0])
        request_products_html = bs(request_products.text,'html.parser')
        comment_box = request_products_html.find_all('div',{'class':'_16PBlm'}) # find all returns list
        logging.debug(comment_box[0].div.div.div.div.text)
        logging.debug(comment_box[0].div.div.find_all('div',{'class':''})[0].div.text)

        count = 0
        for j in comment_box:
            logging.debug("Inside comment_box")
            try:
                logging.debug(j.div.div.div.div.text) #'class':'_3LWZlK _1BLPMq' customer rating
                logging.debug(j.div.div.div.find_all('p',{'class':'_2-N8zT'})[0].text) # comment header
                logging.debug(j.div.div.find_all('div',{'class':''})[0].div.text)
                logging.debug(j.find('div',{'class':'_1LmwT9'}).span.text)
                logging.debug(j.find('p',{'class':'_2sc7ZR _2V5EHH'}).text) # customer name
                logging.debug("\n")

                index = count
                temp_dict = dict()

                name = "name" #+ str(count)
                temp_dict[name]= j.find('p',{'class':'_2sc7ZR _2V5EHH'}).text

                customer_rating = "customer_rating" #+ str(count)
                temp_dict[customer_rating]= j.div.div.div.div.text
                temp_dict[customer_rating] = temp_dict[customer_rating]
                
                comment_header = "comment_header" #+ str(count)
                temp_dict[comment_header]= str(j.div.div.div.find_all('p',{'class':'_2-N8zT'})[0].text)
                temp_dict[comment_header] = temp_dict[comment_header].replace('“','"').replace('”','"')

                customer_comment = "customer_comment" #+ str(count)
                temp_dict[customer_comment]= str(j.div.div.find_all('div',{'class':''})[0].div.text)
                temp_dict[customer_comment] = temp_dict[customer_comment].replace('“','"').replace('”','"')

                likes = "likes" #+ str(count)
                temp_dict[likes]= j.find('div',{'class':'_1LmwT9'}).span.text

                dislikes = "dislikes" #+ str(count)
                temp_dict[dislikes]= j.find('div',{'class':'_1LmwT9 pkR4jH'}).span.text

                comments_data[index] = temp_dict

            except AttributeError:
                logging.error("error")
            count +=1

    with open("output_json.json","w") as jd:
        json.dump(comments_data,jd,indent=4)
    # logging.debug(json.dumps(comments_data))


search_url("iphone11")

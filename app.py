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


# if __name__ == "__main__":
#     app.run(debug=True,host="0.0.0.0",port=5010)
WEBSITE_URL_1 = "https://www.flipkart.com"

comments_data = dict()

def search_url(search_keywords,website=None):
    if website == None:
        website = "www.flipkart.com"
    website_url = f"https://{website}/"
    search_keywords = search_keywords.replace(" ","%20")
    website_url_search = website_url + "search?q=" + search_keywords
    logging.debug(website_url_search)
    url_client = uReq(website_url_search)
    url_page_source = url_client.read()
    url_client.close()
    url_html = bs(url_page_source,'html.parser')
    big_boxes = url_html.find_all("div",{'class':'col-12-12'})
    logging.debug(len(big_boxes)) # length is 33
    # big boxes starts from 8
    # logging.debug(big_boxes[6].find_all('a', 'href'))
    first_page_sub_urls = []
    # finding urls from first page
    for box in url_html.find_all("div",{'class':'col-12-12'}):
        for b in box.find_all("a"):
            temp_string = b.get('href')
            if ".SEARCH" in temp_string:
                first_page_sub_urls.append(temp_string)

    for i in range(len(first_page_sub_urls)):
        first_page_sub_urls[i] = WEBSITE_URL_1 + first_page_sub_urls[i]
    
    logging.debug(f"{first_page_sub_urls[9]} 9th url is the first product link")
    

    logging.debug(first_page_sub_urls)
    logging.debug("length of sub urls: " + str(len(first_page_sub_urls)))

    # grab review links
    # Sample: https://www.flipkart.com/micvir-back-cover-apple-iphone-11/product-reviews/itmd6651646281cf?pid=ACCG856NYKXDGZTK&lid=LSTACCG856NYKXDGZTKEEEVN2&marketplace=FLIPKART
    review_link = [] # link which contains reviews
    request_first_product = requests.get(first_page_sub_urls[0])
    request_first_product_html = bs(request_first_product.text,'html.parser')
    for div in request_first_product_html.find_all("div",{'class':'col-12-12'}):
        for href in div.find_all("a"):
            temp_string = href.get('href')
            if "product-reviews" in temp_string:
                review_link.append(temp_string)
    logging.info(f"Product reviews link is: {review_link}")

    page_number_link = []
    count_page_numbers = 0
    request_page_numbers = requests.get(WEBSITE_URL_1 + review_link[0])
    request_page_numbers_html = bs(request_page_numbers.text,'html.parser')
    for div in request_page_numbers_html.find_all("div",{'class':'col-12-12'}):
        for href in div.find_all("a"):
            temp_string = href.get('href')
            if "&page=" in temp_string:
                count_page_numbers+=1
                page_number_link.append(WEBSITE_URL_1 + temp_string)
    logging.info(f"Product reviews Page numbers: {len(page_number_link)}")

    def loop_review(pages):
        # this function is for one page 
        count = 0
        for page in range(pages):
            request_products = requests.get(page_number_link[page])
            request_products_html = bs(request_products.text,'html.parser')
            comment_box = request_products_html.find_all('div',{'class':'_1AtVbE col-12-12'}) # find all returns list
            # logging.debug(comment_box[0].div.div.div.div.text)
            # logging.debug(comment_box[0].div.div.find_all('div',{'class':''})[0].div.text)
            del comment_box[0:5]
            del comment_box[-1]
            logging.info(f"Total number of comments in box: {len(comment_box)}")

            for j in comment_box:
                logging.debug("Inside comment_box")
                try:
                    # logging.debug(j.div.div.div.div.find('div',{'class':'_3LWZlK _1BLPMq'}).text) #'class':'_3LWZlK _1BLPMq' customer rating 
                    logging.debug(j.div.div.div.div.div)
                    logging.debug(j.div.div.div.div.p.text) # comment header 
                    logging.debug(j.div.div.find_all('div',{'class':''})[0].div.text) # customer_comment
                    logging.debug(j.find('div',{'class':'_1LmwT9'}).span.text) # likes
                    logging.debug(j.find('p',{'class':'_2sc7ZR _2V5EHH'}).text) # customer name
                    logging.debug("\n")

                    index = count
                    temp_dict = dict()

                    name = "name" #+ str(count)
                    temp_dict[name]= j.find('p',{'class':'_2sc7ZR _2V5EHH'}).text

                    customer_rating = "customer_rating" #+ str(count)
                    temp_dict[customer_rating]= j.div.div.div.div.div.text
                    temp_dict[customer_rating] = temp_dict[customer_rating]
                    
                    comment_header = "comment_header" #+ str(count)
                    temp_dict[comment_header]= str(j.div.div.div.div.p.text)
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

        
        # logging.debug(json.dumps(comments_data))
    loop_review(5)



search_url("windows 11")
# search_url("iphone11")
with open("output_json.json","w") as jd:
    json.dump(comments_data,jd,indent=4)

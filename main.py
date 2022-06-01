import bs4
import requests
# from googletrans import Translator
# Translator1= Translator()
# from google_trans_new import google_translator


# translator = google_translator()

#import pyodbc
import ast
import logging
import argparse

# from models.use_use import USECalculator
# from models.use_elmo import ELMoCalculator
# from models.use_bert import BERTCalculator



import os
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import time
from urllib.parse import urlparse, parse_qs
import json

from flask import Flask
#import pyodbc
import ast

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

hostName = "127.0.0.1"
hostPort = 9007

class MyServer(BaseHTTPRequestHandler):
    app = Flask(__name__)

    def startModel(model1, method, verbose, sentences):
        print("in startModel")
        #
        # models = {
        #     # "use": USECalculator,
        #     #  "elmo": ELMoCalculator,
        #     "bert": BERTCalculator,
        # }
        #
        # # if config.model not in models:
        # if model1 not in models:
        #     logging.error(f"The model you chosen is not supported yet.")
        #     return
        #
        # if verbose:
        #     logging.info(f"Loading the corpus...")
        #
        # with open("corpus.txt", "r", encoding="utf-8") as corpus:
        #     sentences = [sentence.replace("\n", "") for sentence in corpus.readlines()]
        #     model = models[model1](method, verbose, sentences)
        #
        #     if verbose:
        #         logging.info(
        #             f'You chose the "{model1.upper()}" as a model.\n'
        #             f'You chose the "{method.upper()}" as a method.'
        #         )
        #
        #     similarity = model.calculate()
        #     print(similarity)
        #     return similarity
        #     if verbose:
        #         logging.info(f"Terminating the program...")

    def getprice(self,url):
        print("here:by faigy b"+url)

        res = requests.get(url,verify=False)
        soup = bs4.BeautifulSoup(res.content, features="html.parser")
        price = soup.find(class_='prices_3bzP').get_text().replace("₪", "")
        if price.__contains__('מ'):
            isfromto = True
        else:
            isfromto = False
        price = "".join(i for i in price if i in " .0123456789")
        list_price = price.split(" ")
        while '' in list_price:
            list_price.remove('')
        list_price = [float(i) for i in list_price]
        if len(list_price) == 2 and isfromto == True:
            list_price.append(-1)
            return list_price
        else:
            return list_price

        pass
    #     do something
    # to use the model you need firefly
    def getDesc(self,url):
        res = requests.get(url,verify=False)
        soup = bs4.BeautifulSoup(res.content, features="html.parser")

        try:
            desc = soup.find(class_='name_20R6').get_text()
            desclist = desc.split('/')
            # translate_text = translator.translate(desclist[0])
            # desclist[0]=translate_text
            # print(translate_text)
        except:
            return (None)
        return desclist
        #
        # descsizelist = []
        # descsizelist.append((desclist[0]))
        # descsizelist.append((size))
        # print(descsizelist)
        #
        # return descsizelist
        # #return desclist[0]



    def do_GET(self):
        # getparams
        query_components = parse_qs(urlparse(self.path).query)
        self.send_response(200)
        self.send_header("Content-type", 'application/json')
        self.end_headers()

        if "getprice" in self.path:
            myUrl = query_components['url'][0]
            pricelist=self.getprice(myUrl)
            json_content = json.dumps(pricelist, ensure_ascii=False)

        if "getDesc" in self.path:
            myUrl = query_components['url'][0]
            desc=self.getDesc(myUrl)
            print("1")
            print(desc)
            print("2")
            json_content = json.dumps(desc, ensure_ascii=False)

        if "startModel" in self.path:
            print("hjkhmnkhbn")
            senetences=["???????????"]
            similarity=self.startModel('bert','angular',True,senetences)

        self.send_response(200)
        self.end_headers()
        #json_content = json.dumps(None, ensure_ascii=False)  # json.dumps(res)
        print(json_content)
        self.wfile.write(bytes(str(json_content), "utf-8"))
        return
    #
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        sentences = self.rfile.read(content_length) # <--- Gets the data itself
        print(sentences)
        self.send_response(200)
        self.end_headers()
        # self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

        # print("ppppooosst")
        # self.parse_request()
        # jsonstr = self.request.POST["Data"]
        # print(jsonstr)
        # self.send_response(200)
        # self.end_headers()
        # return

# generate the server
myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))
try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass
# stop the server
myServer.server_close()
print(time.asctime(), "Server Closed - %s:%s" % (hostName, hostPort))

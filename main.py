# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import bs4
import requests
# from googletrans import Translator

# from google_trans_new import google_translator

#translator = google_translator()

# translate_text1 = translator.translate("חמוד")
# print(translate_text1)




import os
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import time
from urllib.parse import urlparse, parse_qs
import json

from flask import Flask
import pyodbc
import ast

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg


# img = mpimg.imread('your_image.png')
# imgplot = plt.imshow(img)
# plt.show()

hostName = "127.0.0.1"
hostPort = 9007
# url="https://www.terminalx.com/men"
# res = requests.get(url)
# soup = bs4.BeautifulSoup(res.content, features="html.parser")
# price = soup.find(class_='tx-link_29YD')

class MyServer(BaseHTTPRequestHandler):
    app = Flask(__name__)

    def getprice(self,url):
        print("here:by faigy b"+url)


        res = requests.get(url)
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
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.content, features="html.parser")

        try:
            desc = soup.find(class_='name_20R6').get_text()
            desclist = desc.split('/')
            # translate_text = translator.translate(desclist[0])
            # desclist[0]=translate_text
            # print(translate_text)
        except:
            return (None)
        try:
            size = soup.find(class_='size_1bXM').get_text()
            print(size)

        except:
            return (None)
        descsizelist = []
        descsizelist.append((desclist[0]))
        descsizelist.append((size))
        print(descsizelist)

        return descsizelist



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
            print(desc)
            json_content = json.dumps(desc, ensure_ascii=False)
        self.send_response(200)
        self.end_headers()
        #json_content = json.dumps(None, ensure_ascii=False)  # json.dumps(res)
        print(json_content)
        self.wfile.write(bytes(str(json_content), "utf-8"))
        return

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

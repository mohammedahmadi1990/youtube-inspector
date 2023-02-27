from flask import Flask, request, jsonify
from flask_cors import CORS
from YoutubeSearch import YoutubeSearch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import json


app = Flask(__name__)
CORS(app)

youtube = YoutubeSearch('C:\Apps\chrome_110\chromedriver.exe',False)

@app.route('/api', methods=['GET'])
def search():    
    keywords = request.args.get('search')
    # param3 = request.args.get('param3')
    youtube.result_record_count = int(request.args.get('result_record_count'))
    return youtube.run(keywords)

if __name__ == '__main__':
    app.run(debug=True)
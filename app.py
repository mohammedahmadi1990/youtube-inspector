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
    youtube.result_record_count = int(request.args.get('result_record_count'))
    search = request.args.get('search') 
    # print("search:", search)
    youtube.min_subscribers_filter = int(request.args.get('subscriber').split(",")[0])
    # print("min sub:", youtube.min_subscribers_filter)
    youtube.max_subscribers_filter = int(request.args.get('subscriber').split(",")[1])
    # print("max sub:", youtube.max_subscribers_filter)
    youtube.min_views_filter = int(request.args.get('views').split(",")[0])
    # print("min view:", youtube.min_views_filter)
    youtube.max_views_filter = int(request.args.get('views').split(",")[1])
    # print("max view:", youtube.max_views_filter)
    youtube.video_counts_start_filter = int(request.args.get('videos').split(",")[0])
    # print("vid count start:", youtube.video_counts_start_filter)
    youtube.video_counts_end_filter = int(request.args.get('videos').split(",")[1])
    # print("vid count end", youtube.video_counts_end_filter)
    youtube.average_video_views_start_filter = int(request.args.get('average').split(",")[0])
    # print("avg start:", youtube.average_video_views_start_filter)
    youtube.average_video_views_end_filter = int(request.args.get('average').split(",")[1])
    # print("avg end:", youtube.average_video_views_end_filter)
    youtube.location_filter = request.args.get('location')
    # print("location:", youtube.location_filter)
    # youtube.slot = request.args.get('slot')
    return youtube.run(search)

if __name__ == '__main__':
    app.run(debug=True)
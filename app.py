from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import requests
from selenium import webdriver
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi
from bson.objectid import ObjectId

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.jl043qw.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta


# 크롤링할 페이지, indext.html
@app.route('/')
def home():
    return render_template('index.html')


# 크롤링api
@app.route('/test', methods=['POST'])
def test_post():
    url_give = request.form['url_give']

    driver = webdriver.Chrome(url_give)
    # 암묵적으로 웹 지원 로드를 위해 3초까지 기다려준다.
    driver.implicitly_wait(3)
    # url에 접근한다.
    driver.get(url_give)
    html = driver.page_source  ##페이지의 element 모두 가져오기
    soup = BeautifulSoup(html, 'html.parser')

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # data = requests.get(url_give, headers=headers)
    # soup = BeautifulSoup(data.text, 'html.parser')

    contents = soup.select('#contents > div.movie-info-container > div.movie-header-area')
    for content in contents:
        content_title = content.select_one('div > h3').text

    imgs = soup.select('#contents > div.movie-info-container > div')
    for img in imgs:
        bg_image = img.select_one('div.backdrop > img')
        if bg_image is not None:
            bg_url = bg_image['src']
        poster_image = img.select_one('div.poster > img')
        if poster_image is not None:
            poster_url = poster_image['src']

    data_actor = []
    actors_name = soup.select('#synopsis > article > div > div')
    for actor_name in actors_name:
        actors = actor_name.select_one('div.name')
        if actors is not None:
            actor = actors.text
            data_actor.append({'actor': actor})

    Synops = soup.select('#synopsis > article:nth-child(1)')
    for Synop in Synops:
        synop = Synop.select_one('p').text

    data_ott = []
    otts_name = soup.select("#streamingVodList > div > div.price-item-provider > div.provider-info")
    for ott_name in otts_name:
        OTTs = ott_name.select_one('p').text
        data_ott.append({'ott': OTTs})

    years = soup.select('#contents > div> div > div > p')
    for year in years:
        detail = year.select('span')
        year_content = detail[1].text

    doc = {
        'title': content_title,
        'bg_image': bg_url,
        'poster_image': poster_url,
        'actor': data_actor,
        'synop': synop,
        'ott': data_ott,
        'year': year_content,
        'comment_contents': []
        # {'comment': '', 'star': '', 'time': ''}
    }
    db.w4prac_crwaler.insert_one(doc)
    return jsonify({'msg': '저장 완료'})


# 상세페이지, 한줄평저장api
@app.route('/detail/', methods=['POST'])
def detail_comment_post():
    # id_give = request.form['id_give']
    id_give = '63dde3df663cfbf29a97d538'
    comment_give = request.form['comment_give']
    star_give = request.form['star_give']
    time_give = request.form['time_give']

    a = []
    a.append({'comment':comment_give, 'star': star_give, 'time': time_give})

    # db.w4prac_comments.insert_one(comment_content)

    ret = db.w4prac_crwaler.update_one(
        {"_id": ObjectId(id_give)},
         { "$set":{'comment_contents': a}
    }
    )
    print(ret)
    return jsonify({'msg': '한줄평 등록 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)

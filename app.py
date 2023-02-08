from flask import Flask, request, render_template, jsonify
app = Flask(__name__)

from bson.objectid import ObjectId

from pymongo import MongoClient
import certifi
# ca = certifi.where()
# client = MongoClient('mongodb+srv://test:sparta@cluster0.d6xodrs.mongodb.net/Cluster0?retryWrites=true&w=majority',
#                      tlsCAFile=ca)
# db = client.dbsparta
# collection = db["w4prac"]

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.jl043qw.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta
col = db.w4prac_crwaler

import random

@app.route("/")
def index():
    img_txt1 = {
        'image_url': "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdLv8Yn%2FbtrS7uHosPd%2FkZ0g7BJ56oLf5IzWZfGYq0%2Fimg.jpg",
        'text': "<아바타1>를 보고싶었는데 어디서 보냐구요?"}
    img_txt2 = {'image_url': "https://cdn.pixabay.com/photo/2015/10/06/22/04/harry-potter-975362_1280.jpg",
                'text': "<해리포터>를 보고싶었는데 어디서 보냐구요?"}
    img_txt3 = {
        'image_url': "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-1vR6WelpBTgCZd0EOPFhF2FvNtc2DfVQxQ&usqp=CAU",
        'text': "<트랜스포머>를 보고싶었는데 어디서 보냐구요?"}
    img_txt4 = {'image_url': "https://photo.coolenjoy.co.kr/data/editor/1701/Bimg_20170103144951_nhgpcfmf.jpg",
                'text': "<너의 이름은>를 보고싶었는데 어디서 보냐구요?"}

    IMG_TXT = [img_txt1, img_txt2, img_txt3, img_txt4]

    i = random.randrange(0, 4)
    image_url = IMG_TXT[i]['image_url']
    text = IMG_TXT[i]['text']

    return render_template("index.html", image_url=image_url, text=text)

# @app.route("/search", methods=["POST"])
# def search():
#     query = request.form.get("query")
#     results = search_items(query)
#     return render_template("search_results.html", query=query, results=results)
#
# def search_items(query):
#     # col_index = col.create_index([("title", "text")])
#     col_index = col.create_index([("title", "text"), ("image", "text")])
#     # # Search the MongoDB database
#     thumb_list = list(col_index.find({"$text": {"$search": query}}, {"title": 1, "poster_image": 1}))
#     # return [{'title': item['title'], 'image': item['poster_image']} for item in items]
#     return jsonify({'thumbnail': thumb_list})
#
# if __name__ == '__main__':
#    app.run('0.0.0.0', port=6500, debug=True)
@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    results = search_items(query)
    return render_template("search_results.html", query=query, results=results)

def search_items(query):
    col.create_index([("title", "text"), ("poster_image", "text")])

    # Search the MongoDB database
    items = list(col.find({"title": {"$regex": query, "$options": "i"}}))
    print(items)
    return [{'title': item['title'], 'image': item['poster_image']} for item in items]

@app.route("/detail/<item_id>")
def detail(item_id):
    item = col.find_one({"_id": ObjectId(item_id)})
    return render_template("movie_detail.html", item=item)

if __name__ == '__main__':
   app.run('0.0.0.0', port=6500, debug=True)
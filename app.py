from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://denyfebriawan:denyfebriawan@cluster0.bp160w6.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/gudang", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1

    doc = {
        'num' : num,
        'bucket' : bucket_receive,
        'done' : 0
    }

    db.bucket.insert_one(doc)

    return jsonify({'msg': 'data saved!'})
    

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
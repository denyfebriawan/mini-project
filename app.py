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
    item_name_receive = request.form['item_name_give']
    item_quantity_receive = request.form['item_quantity_give']
    count = db.bucket.count_documents({})
    num = count + 1

    doc = {
        'name' : item_name_receive,
        'quantity' : item_quantity_receive,
        
    }

    db.gudangku.insert_one(doc)

    return jsonify({'msg': 'data saved!'})
    

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
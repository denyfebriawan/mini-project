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

    doc = {
        'name' : item_name_receive,
        'quantity' : item_quantity_receive,
        
    }

    db.gudangku.insert_one(doc)

    return jsonify({'msg': 'data saved!'})

@app.route("/gudang", methods=["GET"])
def gudang_get():
    gudangs_list = list(db.gudangku.find({}, {'_id': False}))
    return jsonify({'gudangs': gudangs_list})

@app.route("/delete", methods=["POST"])
def delete_bucket():
    num_receive = request.form['num_give']
    db.bucket.delete_one({'num': int(num_receive)})
    return jsonify({'msg': 'delete done!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
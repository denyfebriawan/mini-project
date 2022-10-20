
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
    count = db.gudangku.count_documents({})
    num = count + 1

    doc = {
        'num': num,
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
    db.gudangku.delete_one({'num': int(num_receive)})
    return jsonify({'msg': 'delete done!'})

@app.route("/increase", methods=['post'])
def increase():
    
    num_receive = request.form['num_give']
    quan_receive = request.form['quan_give']
    inc_quan = int(quan_receive)

    db.gudangku.update_one(
        {'num': int(num_receive)},
        {'$set': {'quantity': inc_quan + 1}}
        )

    return jsonify({'msg': "data increased" })

@app.route("/decrease", methods=['post'])
def decrease():
    
    num_receive = request.form['num_give']
    quan_receive = request.form['quan_give']
    inc_quan = int(quan_receive)

    db.gudangku.update_one(
        {'num': int(num_receive)},
        {'$set': {'quantity': inc_quan - 1}}
        )

    return jsonify({'msg': "data decreased" })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
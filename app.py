from flask import Flask, request, render_template, jsonify, session
from pymongo import MongoClient
from Bcrypt import bcrypt

client = MongoClient('mongodb://denyfebriawan:denyfebriawan@ac-eqp3ojr-shard-00-00.bp160w6.mongodb.net:27017,ac-eqp3ojr-shard-00-01.bp160w6.mongodb.net:27017,ac-eqp3ojr-shard-00-02.bp160w6.mongodb.net:27017/?ssl=true&replicaSet=atlas-jrwx8m-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

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

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
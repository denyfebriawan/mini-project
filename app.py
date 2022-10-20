
from flask import Flask, request, render_template, jsonify, session, redirect, url_for
from pymongo import MongoClient
import bcrypt

client = MongoClient('mongodb://denyfebriawan:denyfebriawan@ac-eqp3ojr-shard-00-00.bp160w6.mongodb.net:27017,ac-eqp3ojr-shard-00-01.bp160w6.mongodb.net:27017,ac-eqp3ojr-shard-00-02.bp160w6.mongodb.net:27017/?ssl=true&replicaSet=atlas-jrwx8m-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)
app.secret_key = 'mysecret'

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

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if request.form['pass'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('home'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            
            db.users.insert_one({'name' : request.form['username'], 'password' :request.form['pass']})
            
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/logout', methods=['get'])
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
   
    app.run(debug=True)
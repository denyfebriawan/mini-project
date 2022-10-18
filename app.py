from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://denyfebriawan:denyfebriawan@cluster0.bp160w6.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
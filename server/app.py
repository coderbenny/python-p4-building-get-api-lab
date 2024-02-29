#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = bakery.to_dict()
        bakeries.append(bakery_dict)
    
    response = make_response(
        jsonify(bakeries),
        200
    )
    
    response.headers["Content-Type"] = 'application/json'
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery_data = Bakery.query.filter_by(id=id).first()
    
    bakery = bakery_data.to_dict()
    
    if bakery_data:
        response = make_response(
            jsonify(bakery),
            200
        )
        response.headers["Content-Type"] = 'application/json'
        return response
    else:
        return jsonify({"error": "Bakery not found"}, 404)
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    all_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    
    goods = [good.to_dict() for good in all_goods ]
    
    if goods:
        response = make_response(
            jsonify(goods),
            200
        )
        response.headers["Content-Type"] = 'application/json'
        return response
    else:
        return jsonify({"error": "No goods found"})

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    
    if baked_goods:
        expensive_good = baked_goods[0]
        exp_good_dict = expensive_good.to_dict()
    
        response = make_response(
            jsonify(exp_good_dict),
            200
        )
        
        response.headers["Content-Type"]='application/json'
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)

from flask import Blueprint, request, jsonify, make_response, session, current_app
import json
from session import session
from datetime import date
from src import db


sellers = Blueprint('sellers', __name__)

# Get all sellers from the DB
@sellers.route('/sellers', methods=['GET'])
def get_sellers():
    cursor = db.get_db().cursor()
    cursor.execute('select s.SellerID, Name FROM Seller s JOIN UserInfo u ON s.SellerID = u.InfoID')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get All Past Sales from this seller with Id userID
@sellers.route('/past_sales', methods=['GET'])
def get_sales():
    cursor = db.get_db().cursor()
    cursor.execute(f'Select o.ProductID, p.ProductName, ListPrice, ListQuantity, BuyerID from Orders o JOIN Products p ON o.ProductID = p.ProductID where FullfillmentStatus = 1 AND o.SellerID = {session.get("sellerID")}')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'

    return the_response

@sellers.route('/new_listing', methods=['POST'])
def make_order():   
    seller = session["sellerID"]
    name = request.form['Name']
    quantity = int(request.form['Quantity'])
    price = float(request.form['Price'])
    ptype = int(request.form['Type'])
    end = request.form['End']
    start = date.today().strftime("%m/%d/%Y")

    current_app.logger.info(seller)
    current_app.logger.info(name)
    current_app.logger.info(quantity)
    current_app.logger.info(price)
    current_app.logger.info(ptype)
    current_app.logger.info(end)

    cursor = db.get_db().cursor()

    cursor.execute(f'INSERT INTO Products (ProductName, SellerID, Quantity, Sale_start, ProductTypeID, unitPrice, Sale_end) VALUES ("{name}", {seller}, {quantity}, "{start}", {ptype}, {price}, "{end}")')

    db.get_db().commit()
    
    return 'Success'
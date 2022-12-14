from flask import Blueprint, request, jsonify, make_response, session, current_app
import json
from datetime import date
from session import session
from src import db


buyers = Blueprint('buyers', __name__)

# Get all buyers from the DB
@buyers.route('/buyers', methods=['GET'])
def get_buyers():
    cursor = db.get_db().cursor()
    cursor.execute('select BuyerID, Name FROM Buyer b JOIN UserInfo u on b.BuyerID = u.InfoID')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get All Orders from user with Id userID
@buyers.route('/buyer_past_orders', methods=['GET'])
def get_orders():
    cursor = db.get_db().cursor()
    buy_id = session['buyerID']
    cursor.execute(f'select o.ProductID, p.ProductName, ListPrice, ListQuantity, o.SellerID from Orders o JOIN Products p ON o.ProductID = p.ProductID where FullfillmentStatus = 1 AND o.BuyerID = {buy_id}')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

  
@buyers.route('/new_user', methods=['POST'])
def new_user():   
    name = request.form['Name']
    address = request.form['Address']
    username = request.form['Username']
    password = request.form['Password']
    email = request.form['Email']

    cursor = db.get_db().cursor()

    cursor.execute(f'INSERT INTO Buyer (Email, UserInfoID) VALUES ("{email}", (SELECT MAX(InfoID) FROM UserInfo) + 1)')
    cursor.execute(f'INSERT INTO Seller (AdministratorID, UserInfoID) VALUES ((SELECT MAX(adminID) FROM Admin), (SELECT MAX(InfoID) FROM UserInfo) + 1)')

    # Insert the user data into the database
    cursor.execute(f'INSERT INTO UserInfo (Address, Name, username, password) VALUES ("{address}", "{name}", "{username}", "{password}")')

    db.get_db().commit()
    
    return 'Success'

@buyers.route('/order', methods=['POST'])
def make_order():   
    product = int(request.form['Product'])
    quantity = int(request.form['Quantity'])
    price = f'SELECT unitPrice FROM Products WHERE ProductID = {product}'
    seller = f'SELECT SellerID FROM Products WHERE ProductID = {product}'
    buyer = session['buyerID']
    address = f'SELECT Address FROM UserInfo WHERE InfoID = {buyer}'
    status = f'CASE WHEN {quantity} > (SELECT Quantity FROM Products WHERE ProductID = {product}) THEN 0 ELSE 1 END' 
    date_t= date.today().strftime("%m/%d/%Y")

    cursor = db.get_db().cursor()

    current_app.logger.info(f'INSERT INTO Orders (SellerID, ProductID, CustAddress, FulfillmentDate, FullfillmentStatus, ListQuantity, ListPrice, BuyerID) VALUES (({seller}), {product}, ({address}), "{date_t}", ({status}), {quantity}, ({price}), {buyer})')

    cursor.execute(f'INSERT INTO Orders (SellerID, ProductID, CustAddress, FulfillmentDate, FullfillmentStatus, ListQuantity, ListPrice, BuyerID) VALUES (({seller}), {product}, ({address}), "{date_t}", ({status}), {quantity}, ({price}), {buyer})')
    db.get_db().commit()
    # Insert the user data into the database
    cursor.execute(f'UPDATE Products p SET Quantity = Quantity - {quantity} WHERE p.ProductID = {product}')

    db.get_db().commit()
    
    return 'Success'

@buyers.route('/login', methods=['POST'])
def login():   
    username = request.form['Username']
    password = request.form['Password']

    userInfo = f'SELECT infoID FROM UserInfo WHERE username = {username} AND password = {password}'
    session['sellerID'] = f'SELECT SellerID FROM Seller WHERE InfoID = ({userInfo})'
    session['buyerID'] = f'SELECT BuyerID FROM Buyer WHERE InfoID = ({userInfo})'

    return 'Success'
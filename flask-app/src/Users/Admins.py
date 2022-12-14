from flask import Blueprint, request, jsonify, make_response, session
import json
from session import session
from src import db


admins = Blueprint('admins', __name__)

# Get all admins from the DB
@admins.route('/admins', methods=['GET'])
def get_admins():
    cursor = db.get_db().cursor()
    cursor.execute('select adminID, username, FROM Admin')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all banned seller ids from the DB
@admins.route('/vendor_bans', methods=['GET'])
def get_vendor_bans():
    cursor = db.get_db().cursor()
    cursor.execute('select vendorID FROM VendorBans')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all banned buyer ids from the DB
@admins.route('/cust_bans', methods=['GET'])
def get_cust_bans():
    cursor = db.get_db().cursor()
    cursor.execute('select custID FROM CustomerBans')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get All Sellers administrated by this admin with id userID
@admins.route('/admin/<userID>', methods=['GET'])
def get_seller_admin(userID):
    cursor = db.get_db().cursor()
    cursor.execute(f'select * from Seller where AdministratorID = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@admins.route('/vendor_ban', methods=['POST'])
def vendor_ban():   
    vendor = int(request.form['Vendor'])
    reason = request.form['Reason']
    admin = session["adminID"]

    cursor = db.get_db().cursor()

    cursor.execute(f'INSERT INTO VendorBans (vendorID, banReason, adminID) VALUES ({vendor}, "{reason}", {admin})')

    db.get_db().commit()
    
    return 'Success'

@admins.route('/cust_ban', methods=['POST'])
def cust_ban():   
    cust = int(request.form['Customer'])
    reason = request.form['Reason']
    admin = session["adminID"]

    cursor = db.get_db().cursor()

    cursor.execute(f'INSERT INTO CustomerBans (custID, banReason, adminID) VALUES ({customer}, "{reason}", {admin})')
    
    db.get_db().commit()
    
    return 'Success'
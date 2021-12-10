import flask
from flask import Flask, jsonify, request, make_response, redirect
import jwt
import datetime
from functools import wraps
from flask_swagger_ui import get_swaggerui_blueprint
from mysql.connector import cursor

from Hotels import locdata
import mysql.connector

import json

# from routes import request_api
app = Flask(__name__)

### swagger specific ###

### end swagger specific ###


# app.register_blueprint(request_api.get_blueprint())



app.config['SECRET_KEY'] = 'mysecretkey'


# Token Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated


# Unprotected Route and function
@app.route('/')
def index():
    return redirect('http://127.0.0.1:5000/login')

# @app.route('/unprotected/<id>',methods=['GET'])
# def unprotected(id):
#     loc= locdata(id)
#     return loc

@app.route('/house/<title>', methods=['GET'])
@app.route('/house/<title>/<bedroom>', methods=['GET'])
@app.route('/house/<title>/<bedroom>/<sleeps>', methods=['GET'])
@app.route('/house/<title>/<bedroom>/<sleeps>/<bathroom>', methods=['GET'])
@app.route('/house/<title>/<bedroom>/<sleeps>/<bathroom>/<price>', methods=['GET'])
@app.route('/house/<title>/<bedroom>/<sleeps>/<bathroom>/<price>/<location>', methods=['GET'])
def house(title='any', bedroom='0', sleeps='0', location='any',bathroom='0',price='0'):

    condo = []

    db_connector = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Scrapping"
    )

    cursor = db_connector.cursor()
# sleep  	bedroom  	bathroom  	price
    query = ("SELECT * FROM datatable WHERE location ="+f"'{location}'  OR price=" + f"'{price}' OR bedroom=" + f"'{bedroom}'OR bathroom=" + f"'{bathroom}' OR sleep=" + f"'{sleeps}'")

    print(query)
    cursor.execute(query)

    results = cursor.fetchall()

    for x in results:
        data = {
            "Title": x[0],
            "Location": x[1],
            "Sleeps": x[2],
            "Bedrooms": x[3],
            "Bathrooms": x[4],
            "Price": x[5],
            "Picture": {
                "Picture_1": x[6][1:-1],
                "Picture_2": x[7][1:-1],
                "Picture_3": x[8][1:-1],
            }

        }
        condo.append(data)

    houseJson = json.dumps(condo, indent=4)
    print(houseJson)
    # print(title, bedroom, sleeps, location)
    return houseJson

# Protected Route and function
@app.route('/protected')
@token_required
def protected():
    #return jsonify({'message': 'Only available to people with valid tokens.'})
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Seans-Python-Flask-REST-Boilerplate"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    return redirect("http://127.0.0.1:5000/swagger",code=302)

# Login Route and function
@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == '1234':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm:"Login Required"'})

# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('static',path)
# app.register_blueprint(requset_api.get.get_blueprint())

if __name__ == "__main__":
    app.run(debug=True)
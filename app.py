from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from helpers import helper #lib with auxiliary functions include in this app

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/mymongodb'
#strat mongo db: C:\Program Files\MongoDB\Server\5.0\bin --> mongod

mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():
    """

    :return:
    """
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if helper.validate_user_to_create(username,password,email):
        respuesta = helper.insert_new_user_mongo(mongo,username,password,email)
    else:
        return not_found()

    return respuesta

@app.route('/users', methods=['GET'])
def get_users():
    response = helper.consult_users(mongo)
    return Response(response,mimetype='application/json')

@app.route('/users/<id_user>', methods=['GET'])
def get_user(id_user):
    response = helper.consult_user_by_id(mongo,id_user)
    return Response(response, mimetype='application/json')

@app.route('/users/<id_user>', methods=['DELETE'])
def delete_user(id_user):
    message = helper.delete_user_by_id(mongo, id_user)
    response = jsonify({'message':message})
    return response

@app.route('/users/<id_user>', methods=['PUT'])
def update_user(id_user):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    validate = helper.validate_user_to_create(username, password, email)
    if validate:
        message = helper.update_user_by_id(mongo, id_user,username,password,email)
        response = jsonify({'message': message})
        return response



@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not found: ' + request.url,
        'status':404
    })
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(debug=True)


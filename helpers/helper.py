from werkzeug.security import generate_password_hash
from bson import json_util
from bson.objectid import ObjectId

def validate_user_to_create(user,password,email):
    if user and email and password:
        return True
    else:
        return False

def insert_new_user_mongo(mongo_ob,user,password,email):
    try:
        hashed_pass = generate_password_hash(password)#encrypting password
        id_mong = mongo_ob.db.users.insert(
            {'username':user,
             'password':hashed_pass,
             'email':email
             }
        )

        #create response to user
        response = {
            '_id': str(id_mong),
            'username': user,
            'password': hashed_pass,
            'email': email
        }

        return response #return object JSON
    except Exception as e:
        print("Error insert new user: ", e)
        return {'message': 'ERROR: User cannot be added',
                'InfoError': e
                }

def consult_users(mongo_ob):
    users = mongo_ob.db.users.find()
    response = json_util.dumps(users)#mongodb object to JSON
    return response

def consult_user_by_id(mongo_ob,id_user):
    response = mongo_ob.db.users.find_one({
        '_id': ObjectId(id_user)#convert id string to objectId mongo
    })
    response= json_util.dumps(response)#to json object
    return response

def delete_user_by_id(mongo, id_user):
    try:
        mongo.db.users.delete_one({
            '_id': ObjectId(id_user)  # convert id string to objectId mongo
        })
        mensaje ='User ' + id_user + ' was Deleted sucessfully'
        print(mensaje)
        return mensaje
    except:
        mensaje ='User ' + id_user + ' could not be found'
        return mensaje

def update_user_by_id(mongo,id_user,name,password,mail):
    hashed_password = generate_password_hash(password)
    mongo.db.users.update_one({'_id': ObjectId(id_user)},
        {'$set':{
        'username':name,
        'password':hashed_password,
        'email':mail
    }})
    mensaje = 'User ' + id_user + ' was Updated sucessfully'
    return mensaje
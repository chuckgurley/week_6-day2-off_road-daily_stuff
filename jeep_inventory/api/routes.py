from flask import Blueprint, request, jsonify
from jeep_inventory.helpers import token_required, random_joke_generator
from jeep_inventory.models import db, Jeep, jeep_schema, jeeps_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
@token_required
def getdata(our_user0):
    return {'some': 'value'}

@api.route('/jeeps', methods = ["POST"])
@token_required
def create_jeep(our_user):
    
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    tire_quality = request.json['tire_quality']
    drive_time = request.json['drive_time']
    max_speed = request.json['max_speed']
    height = request.json['height']
    weight = request.json['weight']
    cost_of_production = request.json['cost_of_production']
    series = request.json['series']
    random_joke = random_joke_generator()
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    jeep = Jeep(name, description, price, tire_quality, drive_time, max_speed, height, weight, cost_of_production, series, random_joke, user_token = user_token )

    db.session.add(jeep)
    db.session.commit()

    response = jeep_schema.dump(jeep)

    return jsonify(response)

#  retrieve (read)all jeeps
@api.route('/jeeps', methods = ['GET'])
@token_required
def get_jeeps(our_user):
    owner = our_user.token
    jeeps = Jeep.query.filter_by(user_token = owner).all()
    response = jeeps_schema.dump(jeeps)

    return jsonify(response)

#retrieve one sigular individual lonely jeep
#jeep
@api.route('/jeeps/<id>', methods = ['GET'])
@token_required
def get_jeep(our_user, id):    
    if id:
        jeep = Jeep.query.get(id)
        response = jeep_schema.dump(jeep)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Id required'}), 401
    
#update jeep by id
@api.route('/jeeps/<id>', methods = ["PUT"])
@token_required
def update_jeep(our_user, id): 
    jeep = Jeep.query.get(id)   
    jeep.name = request.json['name']
    jeep.description = request.json['description']
    jeep.price = request.json['price']
    jeep.tire_quality = request.json['tire_quality']
    jeep.drive_time = request.json['drive_time']
    jeep.max_speed = request.json['max_speed']
    jeep.height = request.json['height']
    jeep.weight = request.json['weight']
    jeep.cost_of_production = request.json['cost_of_production']
    jeep.series = request.json['series']
    jeep.random_joke = random_joke_generator()
    jeep.user_token = our_user.token  

    db.session.commit()

    response = jeep_schema.dump(jeep)

    return jsonify(response)

#DELETE jeep by id
@api.route('/jeeps/<id>', methods = ['DELETE'])
@token_required
def delete_jeeps(current_user, id):
    jeep = Jeep.query.get(id)
    db.session.delete(jeep)
    db.session.commit()

    response = jeep_schema.dump(jeep)
    return jsonify(response)

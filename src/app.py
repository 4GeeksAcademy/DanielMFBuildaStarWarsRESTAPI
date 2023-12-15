"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Person, Favorite, Film, Starship, Vehicle, Species

app = Flask(__name__)
app.url_map.strict_slashes = False

# DATA BASE CONFIG
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DATABASE INITIATE & OTHERS
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# ERRORS HANLD AND SITEMAP


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ENDPOINTS | USERS


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.username for user in users]), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    return jsonify(user.serialize()), 200


@app.route('/users', methods=['POST'])
def create_user():
    body = request.get_json()
    if body is None:
        raise APIException("Request body is missing", status_code=400)
    new_user = User(**body)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"}), 200

# ENDPOINTS | PLANETS


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.name for planet in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    return jsonify(planet.serialize()), 200


@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.get_json()
    if body is None:
        raise APIException("Request body is missing", status_code=400)
    new_planet = Planet(**body)
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"msg": "Planet created successfully"}), 201


@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"msg": "Planet deleted successfully"}), 200

# ENDPOINTS | FILMS


@app.route('/films', methods=['GET'])
def get_films():
    films = Film.query.all()
    return jsonify([film.serialize() for film in films]), 200


@app.route('/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    film = Film.query.get(film_id)
    if film is None:
        raise APIException("Film not found", status_code=404)
    return jsonify(film.serialize()), 200


@app.route('/films', methods=['POST'])
def create_film():
    body = request.get_json()
    if body is None:
        raise APIException("Request body is missing", status_code=400)
    new_film = Film(**body)
    db.session.add(new_film)
    db.session.commit()
    return jsonify({"msg": "Film created successfully"}), 201

# ENDPOINTS | PEOPLE


@app.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()
    return jsonify([person.serialize() for person in people]), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Person.query.get(people_id)
    if person is None:
        raise APIException("Character not found", status_code=404)
    return jsonify(person.serialize()), 200


@app.route('/people', methods=['POST'])
def create_person():
    body = request.get_json()
    if body is None:
        raise APIException("Request body is missing", status_code=400)
    new_person = Person(**body)
    db.session.add(new_person)
    db.session.commit()
    return jsonify({"msg": "Character created successfully"}), 201

# ENDPOINTS | STARSHIPS


@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starship.query.all()
    return jsonify([starship.serialize() for starship in starships]), 200


@app.route('/starships/<int:starship_id>', methods=['GET'])
def get_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if starship is None:
        raise APIException("Starship not found", status_code=404)
    return jsonify(starship.serialize()), 200


@app.route('/starships', methods=['POST'])
def create_starship():
    body = request.get_json()
    if body is None:
        raise APIException("Request body is missing", status_code=400)
    new_starship = Starship(**body)
    db.session.add(new_starship)
    db.session.commit()
    return jsonify({"msg": "Starship created successfully"}), 201

# ENDPOINTS | VEHICLES


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles]), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        raise APIException("Vehicle not found", status_code=404)
    return jsonify(vehicle.serialize()), 200


@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    body = request.get_json()
    if body is None:
        raise APIException("Request body is missing", status_code=400)
    new_vehicle = Vehicle(**body)
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({"msg": "Vehicle created successfully"}), 201

# ENDPOINTS | SPECIES


@app.route('/species', methods=['GET'])
def get_species():
    species = Species.query.all()
    return jsonify([specie.serialize() for specie in species]), 200


@app.route('/species/<int:specie_id>', methods=['GET'])
def get_specie(specie_id):
    specie = Species.query.get(specie_id)
    if specie is None:
        raise APIException("Specie not found", status_code=404)
    return jsonify(specie.serialize()), 200


@app.route('/species', methods=['POST'])
def create_specie():
    body = request.get_json()
    if body is None:
        raise APIException("Request body is missing", status_code=400)
    new_specie = Species(**body)
    db.session.add(new_specie)
    db.session.commit()
    return jsonify({"msg": "Specie created successfully"}), 201



# ENDPOINTS | FAVORITES


@app.route('/favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200


@app.route('/favorites/<int:user_id>', methods=['POST'])
def create_favorite(user_id):
    body = request.get_json()
    if body is None:
        raise APIException("Request body is missing", status_code=400)
    favorite = Favorite(**body, user_id=user_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite created successfully"}), 201


@app.route('/favorites/<int:user_id>', methods=['DELETE'])
def delete_favorite(user_id):
    body = request.get_json()
    if body is None or "favorite_id" not in body:
        raise APIException(
            "Favorite ID is missing in the request body", status_code=400)
    favorite_id = body["favorite_id"]
    favorite = Favorite.query.get((user_id, favorite_id))
    if favorite is None:
        raise APIException("Favorite not found", status_code=404)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted successfully"}), 200


# CONTEXT

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
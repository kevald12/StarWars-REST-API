"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, FavoriteCharacters, FavoritePlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.filter().all()
    result = list(map(lambda user: user.serialize(), users))
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    result = list(map(lambda item: item.serialize(), planets))
    response_body = {
        "msg": "Hello, this is your GET /planets response "
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    result = list(map(lambda item: item.serialize(), characters))
    response_body = {
        "msg": "Hello, this is your GET /characters response "
    }

    return jsonify(response_body), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.filter_by(id = character_id).first()
    response_body = {
    "character": character.serialize()
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.filter_by(id = planet_id).first()
    response_body = {
    "planet": planet.serialize()
    }

    return jsonify(response_body), 200

@app.route('/favoritecharacter/<int:id_character>/<int:id_user>', methods=['POST'])
def post_favoritecharacter(id_character, id_user):
    favorite_character = FavoritesCharacters(user_id=int(id_user), character_id=int(id_character))
    db.session.add(favorite_character)
    db.session.commit()
    response_body = {
    "msg": "favorito agregado exitosamente"
    }
    return jsonify(response_body), 200

@app.route('/favoriteplanet/<int:id_planet>/<int:id_user>', methods=['POST'])
def post_favoriteplanet(id_planet, id_user):
    favorite_planet = FavoritesPlanets(user_id=int(id_user), planet_id=int(id_planet))
    db.session.add(favorite_planet)
    db.session.commit()
    response_body = {
    "msg": "favorito agregado exitosamente"
    }
    return jsonify(response_body), 200


@app.route('/favoritecharacter/<int:id_character>/<int:id_user>', methods=['DELETE'])
def delete_favorite_character(id_character, id_user):
    favorite_character = FavoritesCharacters.filter_by(user_id=int(id_user), character_id=int(id_character))
    if favorite_character is None:
        return jsonify ({"msg":"no se encontro el favorito character"})
    db.session.delete(favorite_character)
    db.session.commit()
    response_body = {
    "msg":"favorito character eliminado exitosamente"
    }
    return jsonify(response_body), 200

@app.route('/favoriteplanet/<int:id_planet>/<int:id_user>', methods=['DELETE'])
def delete_favorite_planet(id_planet, id_user):
    favorite_planet = FavoritesPlanets.filter_by(user_id=int(id_user), planet_id=int(id_planet))
    if favorite_planet is None:
        return jsonify ({"msg":"no se encontro el favorito planeta"})
    db.session.delete(favorite_planet)
    db.session.commit()
    response_body = {
    "msg":"favorito planeta eliminado exitosamente"
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

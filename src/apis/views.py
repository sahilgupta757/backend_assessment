import logging
from flask import request, jsonify
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


logger = logging.getLogger("default")


def index():
    logger.info("Checking the flask scaffolding logger")
    return "Welcome to the flask scaffolding application"


def create_user():
    data = request.get_json()
    user = User.objects(username=data.get('username')).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400
    pw = generate_password_hash(password=data.get('password'), method="sha256", salt_length=8)
    new_user = User(data.get('username'), pw)
    new_user.save()
    return jsonify({'message': 'User created successfully'}), 201


def login():
    """
    TASKS: write the logic here to parse a json request
           and send the parsed parameters to the appropriate service.

           return a json response and an appropriate status code.
    """

    data = request.get_json()
    user = User.objects(username=data.get('username')).first()
    if user:
        auth = check_password_hash(pwhash=user.password, password=data.get('password'))
        if auth is False:
            return jsonify({"message": "username or password does not match, please try again"}), 401
        return jsonify({"message": "User has logged in successfully"}), 200
    return jsonify({"message": "User does not exist"}), 400



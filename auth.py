from flask import Blueprint,jsonify,request
from models import User,TokenBlocklist
from extensions import logger
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity)
auth_bp=Blueprint("auth",__name__)

@auth_bp.post('/register')
def register_user():
    data=request.get_json()
    user=User.get_user_by_username(username=data.get('username'))

    if user is not None:
        logger.warning(f"Registration failed: User '{data.get('username')}' already exists.")
        return jsonify({"error":"user already exists"}),409
    new_user=User(
        username=data.get('username'),
        email=data.get('email')
        )
    new_user.set_password(password=data.get('password'))
    new_user.save()
    logger.info(f"User '{new_user.username}' registered successfully.")
    return jsonify({"message":"User Created"}),201


@auth_bp.post('/login')
def login_user():
    data=request.get_json()
    user=User.get_user_by_username(username=data.get('username'))

    if user and (user.check_password(password=data.get('password'))):
        access_token=create_access_token(identity=user.username)
        refresh_token=create_refresh_token(identity=user.username)
        logger.info(f"User '{user.username}' logged in successfully.")
        return jsonify(
            {
            "message":"Logged In successfully",
             "tokens":{
                 "access":access_token,
                 "refresh":refresh_token
                }
        }),200
    logger.warning(f"Login failed: Invalid credentials for username '{data.get('username')}'.")
    return jsonify({"error":"Invalid credentials"}),400



# @auth_bp.get('/whoami')
# @jwt_required()
# def whoami():
#     claims=get_jwt()
#     return jsonify({"message":"Its me","claims":claims}),200

@auth_bp.get('/whoami')
@jwt_required()
def whoami():
    # claims=get_jwt()
    return jsonify({"message":"Its me","user_details":{"username":current_user.username,"email":current_user.email}}),200


@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    identity=get_jwt_identity()
    new_access_token=create_access_token(identity=identity)
    return jsonify({"access token":new_access_token}),200

@auth_bp.get("/logout")
@jwt_required(refresh=False)
def logout():
    jwt=get_jwt()
    jti=jwt["jti"]
    token_type=jwt["type"]
    token_b=TokenBlocklist(jti=jti)
    token_b.save()
    return  jsonify({"message":f"{token_type} token has been revoked",}),200

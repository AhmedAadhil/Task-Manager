from flask import Flask,jsonify
from extensions import db,jwt
from auth import auth_bp
from users import user_bp
from models import User,TokenBlocklist
from routes import routes
from tasks import tasks_bp  
def create_app():

    app=Flask(__name__)

    #initializing externals
    app.config.from_prefixed_env()

    #initializing db and jwt
    db.init_app(app)
    jwt.init_app(app)



    #registering blueprints
    app.register_blueprint(auth_bp,url_prefix="/auth")
    app.register_blueprint(user_bp,url_prefix="/users")
    app.register_blueprint(tasks_bp, url_prefix="/api")
    app.register_blueprint(routes)

    #jwt load user , im using this to load details of current user
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header,jwt_data):
        identity=jwt_data["sub"]
        return User.query.filter_by(username=identity).one_or_none()


    #additional claims
    #i am setting custom addtional attributes(claims) to the jwt token 
    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        if(identity=="admin"):
            return {"is_admin":True}
        return {"is_admin":False}


    #jwt error handling
    #here i am creating error handling methods for jwt
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_data):
        return jsonify({"message":"token has expired","error":"token_expired"}),401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message":"token is invalid","error":"token_invalid"}),401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message":"request does not contain a valid token","error":"unauthorized_header"}),401

    
    #checking whether given user token is in blocklist ,if no then it returns True
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header,jwt_data):
        jti=jwt_data["jti"]
        token=db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()

        return token is not None
    
    return app
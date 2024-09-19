from flask import Flask, jsonify
from flask_smorest import Api
import os

from db import db
import models
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from database.item import blp as ItemBlueprint
from database.store import blp as StoreBlueprint
from database.tag import blp as TagBluePrint
from database.user import blp as UserBluePrint

from blocklist import BLOCKLIST

def create_app(db_url= None):
  app = Flask(__name__)

  app.config["PROPAGATE_EXCEPTIONS"] = True
  app.config["API_TITLE"] = "Stores REST API"
  app.config["API_VERSION"] = "v1"
  app.config["OPENAPI_VERSION"] = "3.0.3"
  app.config["OPENAPI_URL_PREFIX"] = "/"
  app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
  app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.init_app(app)

  migrate = Migrate(app, db)
  api = Api(app)


  app.config["JWT_SECRET_KEY"] = "3406857207503645503"
  jwt = JWTManager(app)


  @jwt.token_in_blocklist_loader
  def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST
  
  @jwt.revoked_token_loader
  def revoked_token_callback(jwt_header, jwt_payload):
    return (
      jsonify(
          {"description": "The token has been revoked.", "error": "token_revoked"}
      ),
      401,
    )

  @jwt.additional_claims_loader
  def add_claims_to_jwt(identity):
    if identity == 1:
      return {"is_admin": True}
    return {"is_admin": False}

  @jwt.expired_token_loader
  def expired_token_callback(jwt_header, jwt_payload):
    return (
      jsonify({"message": "The token has expired.", "error": "token_expired"}),
      401,
    )

  @jwt.invalid_token_loader
  def invalid_token_callback(error):
    return (
      jsonify(
        {"message": "Signature verification failed.", "error": "invalid_token"}
      ),
      401,
    )

  @jwt.unauthorized_loader
  def missing_token_callback(error):
    return (
      jsonify(
        {
          "description": "Request does not contain an access token.",
          "error": "authorization_required",
        }
      ),
      401,
    )



  with app.app_context():
    db.create_all()

  api.register_blueprint(ItemBlueprint)
  api.register_blueprint(StoreBlueprint)
  api.register_blueprint(TagBluePrint)
  api.register_blueprint(UserBluePrint)
  
  return app




#! if we want make migration folder we should enter flask db init in terminal
#! after that we enter flask db migrate
#! after then we enter flask db upgrede
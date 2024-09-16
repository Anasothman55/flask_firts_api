
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha512
from schemas import UserSchema
from db import db
from models import UserModel

from sqlalchemy.exc import SQLAlchemyError,IntegrityError



blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
  @blp.arguments(UserSchema)
  def post(self, user_data):
    
    if UserModel.query.filter(UserModel.username == user_data["username"]).first():
      abort(409, message = "A user with that username already exists.")
    
    user = UserModel(
      username = user_data["username"],
      password = pbkdf2_sha512.hash(user_data["password"])
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "User create successfuly"}, 201
  
@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
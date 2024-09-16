import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

blp = Blueprint("store", __name__, description="Operation on store")



@blp.route("/store/<int:store_id>")
class Store(MethodView):

  @blp.response(200, StoreSchema)
  def get(self, store_id):
    store = StoreModel.query.get_or_404(store_id)
    return store

  def delete(self, store_id):
    store = StoreModel.query.get_or_404(store_id)
    db.session.delete(store)
    db.session.commit()
    
    return {"message": "The store deleted"}
  


@blp.route("/store")
class StoreList(MethodView):

  @blp.response(200, StoreSchema(many=True))
  def get(self):
    store = StoreModel.query.all()
    return store
  
  @blp.arguments(StoreSchema)
  @blp.response(201, StoreSchema)
  def post(self, store_data):

    store = StoreModel(**store_data)

    try:
      db.session.add(store)
      db.session.commit()
    except IntegrityError:
      abort(400, message="Store already exists")
    except SQLAlchemyError:
      abort(500, message="An error accurred while inserting store")
      
    return store, 201
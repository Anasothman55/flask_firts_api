from flask_jwt_extended import jwt_required,get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

blp = Blueprint("items", __name__, description = "Operation on Items")


@blp.route("/items")
class ItemList(MethodView):
  
  @jwt_required(fresh=True)
  @blp.arguments(ItemSchema)
  @blp.response(201, ItemSchema)
  def post(self, request_data):

    item = ItemModel(**request_data)

    try:
      db.session.add(item)
      db.session.commit()
    except IntegrityError:
      abort(400, message="Item already exists")
    except SQLAlchemyError:
      abort(500, message="An error accurred while inserting item")
      
    return item, 201
  

  
  @blp.response(200, ItemSchema(many=True))
  def get(self):
    item = ItemModel.query.all()
    return item
  

@blp.route("/items/<string:item_id>")
class Items(MethodView):

  @blp.response(200, ItemSchema)
  def get(self, item_id):
    item = ItemModel.query.get_or_404(item_id)
    return item

  @jwt_required()
  def delete(self, item_id):
    jwt = get_jwt()
    if not jwt.get("is_admin"):
      abort(401, message="Admin privilege required")
    item = ItemModel.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    
    return {"message": "The Item deleted"}
  

  @blp.arguments(ItemUpdateSchema)
  @blp.response(200, ItemSchema)
  def put(self, request_data, item_id):

    item = ItemModel.query.get(item_id)
    if item:
      item.price = request_data["price"]
      item.name = request_data["name"]
    else:
      item = ItemModel(id= item_id ,**request_data)

    db.session.add(item)
    db.session.commit()

    return item


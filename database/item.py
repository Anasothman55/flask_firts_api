import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items,stores



blp = Blueprint("items", __name__, description = "Operation on Items")



@blp.route("/items")
class ItemList(MethodView):
  def post(self):
    
    request_data = request.get_json()

    if "price" not in request_data or "store_id" not in request_data or "name" not in request_data:
      abort(400,message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",)

    for item in items.values():
      if (request_data["name"] == item["name"] and request_data["store_id"] == item["store_id"]):
        abort(400, message=f"Item already exists.")

    if request_data["store_id"] not in stores:
      abort(400, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**request_data, "id": item_id}
    items[item_id] = item
    return item, 201
  

  def get(self):
    return {"Items": list(items.values())}
  

@blp.route("/items/<string:item_id>")
class Items(MethodView):

  def get(self, item_id):
    try:
      return {"id": items[item_id]["id"], "data":items[item_id]}, 200
    except KeyError: 
      abort(404, message="Store not found")
  

  def delete(self, item_id):
    try:
      del items[item_id]
      return {"message":"Item deleted"}
    except KeyError: 
      abort(404, message="Item not found")


  def put(self, item_id):
    
    request_data = request.get_json()

    if "price" not in request_data or "name" not in request_data:
      abort(400,message="Bad request. Ensure 'price' and 'name' are included in the JSON payload.",)

    try:
      
      for item in items.values():
        if (request_data["name"] == item["name"]):
          abort(400, message="Item already exists.")
      
      putitem = items[item_id]
      putitem |= request_data
      
      return putitem
    except KeyError:
      abort(400, message=f"Item not found.")


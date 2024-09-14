from flask import Flask, request
from db import items,stores
import uuid
from flask_smorest import abort


app = Flask(__name__)



@app.get("/store")
def get_stores():
  return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
  store_data = request.get_json()
  if "name" not in store_data:
    abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.", )

  for store in stores.values():
    if store_data["name"] == store["name"]:
      abort(400, message=f"Store already exists.")

  store_id = uuid.uuid4().hex
  store = {**store_data, "id": store_id}
  stores[store_id] = store

  return store


@app.post("/items")
def create_item():
  
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


@app.get("/items")
def get_items():
  return {"Items": list(items.values())}



@app.get("/store/<string:store_id>")
def get_store_data(store_id):
  try:
    return stores[store_id], 200
  except KeyError: 
    abort(404, message="Store not found")

@app.delete("/store/<string:store_id>")
def delete__store_data(store_id):
  try:
    del stores[store_id]
    return {"message":"store deleted"}
  except KeyError: 
    abort(404, message="Store not found")
  

@app.get("/items/<string:item_id>")
def get__item_data(item_id):
  try:
    return {"id": items[item_id]["id"], "data":items[item_id]}, 200
  except KeyError: 
    abort(404, message="Store not found")
  

@app.delete("/items/<string:item_id>")
def delete__item_data(item_id):
  try:
    del items[item_id]
    return {"message":"Item deleted"}
  except KeyError: 
    abort(404, message="Item not found")
  


@app.put("/items/<string:item_id>")
def update_item(item_id):
  
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



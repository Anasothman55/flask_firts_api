from db import db


class ItemTag(db.Model):
  __tablename__ = 'item_tags'

  id = db.Column(db.Integer, primary_key=True)
  item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
  tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
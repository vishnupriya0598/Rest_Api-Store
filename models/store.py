#import sqlite3
from db import db

class StoreModel(db.Model): #similar to ItemModel
     __tablename__='stores'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80))

    items=db.relationship('ItemModel',lazy='dynamic') #lazy-for not creating a massive list of objects for all items


    def __init__(self,name):
        self.name=name

    def json(self):
        return {'name':self.name,'items':[item.json() for item in self.items.all()]} #returns all items having same store_id

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() #similar to select query


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

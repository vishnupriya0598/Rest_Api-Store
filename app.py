# coding: utf-8
# Your code here!
import os

from db import db
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList


app=Flask(__name__)

app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL','sqlite:///data.db') #SQLAlchemy creates a db and place in data.db so no need to use create_tables.py
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #Avoid changes
app.secret_key='xyz'
api=Api(app)

jwt=JWT(app,authenticate,identity) #/auth

#items=[]

api.add_resource(Item,'/item/<string:name>')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister,'/register')

if __name__=='__main__':
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
    #app.run(port=5000,debug=True)

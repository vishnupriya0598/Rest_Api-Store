from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
      parser=reqparse.RequestParser()
        parser.add_argument('price',
            type=float,
            required=True,
            help="This is mandatory field"
        )
        parser.add_argument('store_id',
            type=int,
            required=True,
            help="This is mandatory field"
        )


    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'},404
        #item=next(filter(lambda x:x['name']==name,items),None)
        #for item in items:
           # if item['name']==name:
             #   return item

    def post(self,name):
        #if(next(filter(lambda x:x['name']==name,items),None))is not None:
        if ItemModel.find_by_name(name):
            return {'message':"An item with name '{}' already exits".format(name)},400 #400-Bad request
        request_data=Item.parser.parse_args()

        item=ItemModel(name,**request_data)

        try:
            item.save_to_db()
        except:
            return {'message':'Error occured in creating'},500 #500-Internal server error
        return item.json(),201 #201-Created
        #if row:
         #   return {'item':{'name':row[0],'price':row[1]}}
        #items.append(item)


    def delete(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':'Item deleted'}
        return {'message':'Item not found'}

        '''connection=sqlite.connect('data.db')
        cursor=connection.cursor()

        query="DELETE FROM items WHERE name=?" #delete a particular item
        cursor.execute(query,(name,))

        connection.commit()
        connection.close()
        #global items
        #items=list(filter(lambda x:x['name']!=name,items))
        return {'message':'Item deleted'}'''


    def put(self,name):
        request_data=Item.parser.parse_args()

        item=ItemModel.find_by_name(name)
        #updated_item=ItemModel(name,request_data['price']
        #request_data=request.get_json()
        #item=next(filter(lambda x:x['name']==name,items),None)
        if item is None:
            item=ItemModel(name,**request_data)
            '''try:
               updated_item.insert()
            except:
                return {'message':'Error occured in creating'},500 #500-Internal server error
            #item={'name':name,'price':request_data['price']}
            #items.append(item)'''
        else:
            item.price=request_data['price']
            '''try:
                updated_item.update()
            except:
                return {'message':'Error occured in creating'},500 #500-Internal server error
            #item.update(request_data)'''
        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items':[x.json() for x in ItemModel.query.all()]}

        '''connection=sqlite.connect('data.db')
           cursor=connection.cursor()

           query="SELECT * FROM items"
           result =cursor.execute(query)
           items=[]
           for row in result:
           items.append({'name':row[0],'price':row[1]})

           connection.close()
           return {'items':items}'''

import os
import socket
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api, abort
from flask_pymongo import PyMongo
from bson import ObjectId

app= Flask(__name__)
api=Api(app)

app.config["MONGO_URI"] = "mongodb://mongo:27017/dev"
mongo = PyMongo(app)
db = mongo.db

@app.route('/')
def index():
    hostname = socket.gethostname()
    return jsonify(
        message="Welcome to Tasks app! I am running inside {} pod!".format(hostname)
    )

class ToDo(Resource):
    def get(self):
        tasks = db.task.find()
        data = []
        for task in tasks:
            item = {
                'id': str(task['_id']),
                "task": task["task"],
                'status': task['status']
            }
            data.append(item)
        return jsonify(data=data)
    
    def post(self):
        data = request.get_json(force=True)
        item = {
            "task": data["task"],
            'status': False
        }
        db.task.insert_one(item)
        return make_response(jsonify(status=True,message='To-do saved successfully!'), 201)

    def delete(self):
        db.task.delete_many({})
        return make_response(jsonify(message='TODO Cleared!'), 204)    


class TodoTask(Resource):
    def get(self, id):
        data= db.task.find_one({"_id": ObjectId(id)}) 
        item = {
                'id': str(data['_id']),
                'task': data['task'],
                'status': data['status']
            }
        return make_response(jsonify(item), 201)

    def delete(self,id):
        db.task.delete_one({"_id": ObjectId(id)}) 
        return make_response(jsonify(message='Deleted Task successfully!'), 204)
    
    def put(self, id):
        task1=db.task.find_one({"_id": ObjectId(id)}) 
        if task1:
            if task1["status"]==True:    
                db.task.update_one({"_id": ObjectId(id)}, {"$set": {"status":False}})    
            else:    
                db.task.update_one({"_id": ObjectId(id)}, {"$set": {"status":True}})    
            return make_response(jsonify(status=True,message='Status Updated!'), 204)
        else:
            abort(404, message="Task doesn't exist")

api.add_resource(ToDo, '/todo')
api.add_resource(TodoTask, '/task/<id>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

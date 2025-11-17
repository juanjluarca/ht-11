from bson import ObjectId
from database import get_db

db = get_db()
proyectos = db["proyectos"]
encargados = db["encargados"]

# proyectos

def get_all_projects():
  return list(proyectos.find())

def add_project(data):
  proyectos.insert_one(data)

def update_project(project_id, data):
  proyectos.update_one(
    {"_id": ObjectId(project_id)},
    {"$set": data}
  )

def get_project_with_details(project_id):
  return proyectos.find_one({"_id": ObjectId(project_id)})

def delete_project(project_id):
  proyectos.delete_one({"_id": ObjectId(project_id)})
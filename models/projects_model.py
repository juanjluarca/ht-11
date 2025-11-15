from bson import ObjectId
from database import get_db

db = get_db()
proyectos = db["proyectos"]
encargados = db["encargados"]

def get_all_projects():
  return {}
from bson import ObjectId
from datetime import datetime
from database import get_db

db = get_db()
encargados = db["encargados"]

def get_all_encargados():
    return list(encargados.find())

def get_encargado_by_id(encargado_id):
    return encargados.find_one({"_id": ObjectId(encargado_id)})

def get_encargado_by_dpi(dpi):
    return encargados.find_one({"dpi": dpi})

def create_encargado(nombre, direccion, dpi):
    if get_encargado_by_dpi(dpi):
        return None, "Ya existe un encargado con ese DPI"
    
    encargado = {
        "nombre": nombre,
        "direccion": direccion,
        "dpi": dpi,
        "proyectos_activos": 0.0,
        "proyectos_finalizados": 0.0,
        "presupuesto_total_manejado": 0.0,
        "creado_en": datetime.now()
    }
    
    result = encargados.insert_one(encargado)
    return result.inserted_id, None

def update_encargado(encargado_id, nombre, direccion, dpi):
    existing = encargados.find_one({"dpi": dpi, "_id": {"$ne": ObjectId(encargado_id)}})
    if existing:
        return False, "Ya existe otro encargado con ese DPI"
    
    result = encargados.update_one(
        {"_id": ObjectId(encargado_id)},
        {"$set": {
            "nombre": nombre,
            "direccion": direccion,
            "dpi": dpi
        }}
    )
    
    return result.modified_count > 0, None

def delete_encargado(encargado_id):
    result = encargados.delete_one({"_id": ObjectId(encargado_id)})
    return result.deleted_count > 0

def update_encargado_stats(encargado_id, proyectos_activos=None, proyectos_finalizados=None, presupuesto_total=None):
    update_fields = {}
    
    if proyectos_activos is not None:
        update_fields["proyectos_activos"] = float(proyectos_activos)
    if proyectos_finalizados is not None:
        update_fields["proyectos_finalizados"] = float(proyectos_finalizados)
    if presupuesto_total is not None:
        update_fields["presupuesto_total_manejado"] = float(presupuesto_total)
    
    if update_fields:
        result = encargados.update_one(
            {"_id": ObjectId(encargado_id)},
            {"$set": update_fields}
        )
        return result.modified_count > 0
    
    return False
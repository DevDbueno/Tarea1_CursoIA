
#region Imports

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

#endregion

#region Configuración de la base de datos

Base = declarative_base()
engine = create_engine('sqlite:///tareas.db') 
Session = sessionmaker(bind=engine)
session = Session()
#endregion

#region Modelo de la tarea y creación	

class Tarea(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    completada = Column(Boolean, default=False)

Base.metadata.create_all(engine)
#endregion

#region Metodos para manejo de la Tarea
def agregar_tarea():
    titulo = input("Título de la tarea: ")
    descripcion = input("Descripción de la tarea: ")
    nueva_tarea = Tarea(titulo=titulo, descripcion=descripcion)
    session.add(nueva_tarea)
    session.commit()
    print("Tarea agregada con éxito.")

def listar_tareas():
    tareas = session.query(Tarea).all()
    if not tareas:
        print("No hay tareas.")
    for tarea in tareas:
        estado = "Completada" if tarea.completada else "Pendiente"
        print(f"[{tarea.id}] {tarea.titulo} - {estado}\nDescripción: {tarea.descripcion}")

def marcar_completada():
    listar_tareas()
    tarea_id = int(input("ID de la tarea a marcar como completada: "))
    tarea = session.query(Tarea).filter_by(id=tarea_id).first()
    if tarea:
        tarea.completada = True
        session.commit()
        print("Tarea marcada como completada.")
    else:
        print("Tarea no encontrada.")

def eliminar_tareas_completadas():
    tareas_completadas = session.query(Tarea).filter_by(completada=True).all()
    if not tareas_completadas:
        print("No hay tareas completadas para eliminar.")
    else:
        for tarea in tareas_completadas:
            session.delete(tarea)
        session.commit()
        print("Tareas completadas eliminadas.")

def guardar_tareas():
    tareas = session.query(Tarea).all()
    tareas_dict = [
        {"id": tarea.id, "titulo": tarea.titulo, "descripcion": tarea.descripcion, "completada": tarea.completada}
        for tarea in tareas
    ]
    with open("tareas.json", "w") as archivo:
        json.dump(tareas_dict, archivo)
    print("Tareas guardadas en tareas.json.")

def cargar_tareas():
    try:
        with open("tareas.json", "r") as archivo:
            tareas_dict = json.load(archivo)
        for tarea_data in tareas_dict:
            tarea = Tarea(
                titulo=tarea_data["titulo"],
                descripcion=tarea_data["descripcion"],
                completada=tarea_data["completada"]
            )
            session.merge(tarea)  # Merge evita duplicados
        session.commit()
        print("Tareas cargadas desde tareas.json.")
    except FileNotFoundError:
        print("Archivo tareas.json no encontrado. No se cargaron tareas.")

#endregion

#region Menú principal
def menu():
    cargar_tareas()  
    while True:
        print("\nGestión de Tareas")
        print("1. Agregar tarea")
        print("2. Listar tareas")
        print("3. Marcar tarea como completada")
        print("4. Eliminar tareas completadas")
        print("5. Guardar tareas")
        print("6. Salir")
        opcion = input("Selecciona una opción: ")

        try:
            if opcion == "1":
                agregar_tarea()
            elif opcion == "2":
                listar_tareas()
            elif opcion == "3":
                marcar_completada()
            elif opcion == "4":
                eliminar_tareas_completadas()
            elif opcion == "5":
                guardar_tareas()
            elif opcion == "6":
                print("Saliendo de la aplicación.")
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")
        except Exception as e:
            print(f"Se produjo un error: {e}")

if __name__ == "__main__":
    menu()
    
#endregion

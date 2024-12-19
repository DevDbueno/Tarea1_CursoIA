
#region Imports

from tkinter import Tk, Label, Button, Listbox, Scrollbar, Entry, END, messagebox, StringVar, Toplevel
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

#region Menú principal
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Tareas")
        self.root.geometry("500x600")

        Label(self.root, text="Gestor de Tareas", font=("Arial", 16, "bold")).pack(pady=10)

        self.lista_tareas = Listbox(self.root, width=50, height=15)
        self.lista_tareas.pack(pady=10)

        scrollbar = Scrollbar(self.root)
        self.lista_tareas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.lista_tareas.yview)
        scrollbar.pack(side="right", fill="y")

        Button(self.root, text="Agregar Tarea", command=self.ventana_agregar).pack(pady=5)
        Button(self.root, text="Marcar como Completada", command=self.marcar_completada).pack(pady=5)
        Button(self.root, text="Eliminar Completadas", command=self.eliminar_completadas).pack(pady=5)
        Button(self.root, text="Guardar en JSON", command=self.guardar_tareas).pack(pady=5)
        Button(self.root, text="Cargar desde JSON", command=self.cargar_tareas).pack(pady=5)
        Button(self.root, text="Salir", command=self.root.quit).pack(pady=5)

        self.listar_tareas()
    def ventana_agregar(self):
        agregar_win = Toplevel(self.root)
        agregar_win.title("Agregar Tarea")
        agregar_win.geometry("300x200")

        Label(agregar_win, text="Título:").pack(pady=5)
        titulo_entry = Entry(agregar_win, width=30)
        titulo_entry.pack(pady=5)

        Label(agregar_win, text="Descripción:").pack(pady=5)
        descripcion_entry = Entry(agregar_win, width=30)
        descripcion_entry.pack(pady=5)

        def guardar():
            titulo = titulo_entry.get()
            descripcion = descripcion_entry.get()
            if titulo:
                nueva_tarea = Tarea(titulo=titulo, descripcion=descripcion)
                session.add(nueva_tarea)
                session.commit()
                self.listar_tareas()
                messagebox.showinfo("Éxito", "Tarea agregada con éxito")
                agregar_win.destroy()
            else:
                messagebox.showerror("Error", "El título es obligatorio")

        Button(agregar_win, text="Guardar", command=guardar).pack(pady=10)
    def listar_tareas(self):
        self.lista_tareas.delete(0, END)
        tareas = session.query(Tarea).all()
        for tarea in tareas:
            estado = "Completada" if tarea.completada else "Pendiente"
            self.lista_tareas.insert(END, f"[{tarea.id}] {tarea.titulo} - {estado}")

    def marcar_completada(self):
        try:
            seleccion = self.lista_tareas.get(self.lista_tareas.curselection())
            tarea_id = int(seleccion.split("]")[0][1:])
            tarea = session.query(Tarea).filter_by(id=tarea_id).first()
            if tarea:
                tarea.completada = True
                session.commit()
                self.listar_tareas()
                messagebox.showinfo("Éxito", "Tarea marcada como completada")
        except Exception:
            messagebox.showerror("Error", "Selecciona una tarea de la lista")

    def eliminar_completadas(self):
        tareas_completadas = session.query(Tarea).filter_by(completada=True).all()
        for tarea in tareas_completadas:
            session.delete(tarea)
        session.commit()
        self.listar_tareas()
        messagebox.showinfo("Éxito", "Tareas completadas eliminadas")

    def guardar_tareas(self):
        tareas = session.query(Tarea).all()
        tareas_dict = [{"id": t.id, "titulo": t.titulo, "descripcion": t.descripcion, "completada": t.completada}
                       for t in tareas]
        with open("tareas.json", "w") as archivo:
            json.dump(tareas_dict, archivo)
        messagebox.showinfo("Éxito", "Tareas guardadas en tareas.json")

    def cargar_tareas(self):
        try:
            with open("tareas.json", "r") as archivo:
                tareas_dict = json.load(archivo)
            for tarea_data in tareas_dict:
                tarea = Tarea(titulo=tarea_data["titulo"],
                              descripcion=tarea_data["descripcion"],
                              completada=tarea_data["completada"])
                session.merge(tarea)
            session.commit()
        except:
            messagebox.showinfo("Error", "No existen tareas en tareas.json")
            pass

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
    
#endregion

Para la próxima clase como tareas estudiar sobre conceptos básicos con Python	Semana 1
"Desarrolla una Aplicación de Gestión de Tareas

Crea una aplicación en Python que permita a los usuarios gestionar sus tareas diarias. La aplicación debe incluir las siguientes funcionalidades:

1. Agregar Tareas:
        Permitir al usuario agregar nuevas tareas con un título y una descripción.
2. Listar Tareas:
        Mostrar todas las tareas agregadas con su estado (pendiente o completada).
3. Marcar Tareas como Completadas:
        Permitir al usuario marcar una tarea como completada.
4. Eliminar Tareas:
        Permitir al usuario eliminar tareas completadas.
5. Guardar y Cargar Tareas:
        Guardar las tareas en un archivo y cargar las tareas desde un archivo al iniciar la aplicación.

Requisitos Técnicos:

* Utiliza estructuras de datos como listas y diccionarios.
* Maneja excepciones para asegurar que la aplicación no se cierre inesperadamente.
* Utiliza módulos estándar de Python como json para importar y exportar tareas.
* Utiliza una conexión a una base de datos sql para tener persistencia de datos (Puedes usar SQLAlchemy)."


Solución de la Implementación explicado por #Region

1. Región Imports

Aqui se encuentran todas las librerias y paquetes necesarios importados e implementados para el funcionamiento y ejecución del codigo

2. Configuración de la base de datos

Se instancia el servicio de la base de datos y se crea la implementación con SQLAlchemy

3. Modelo de la tarea y creación

En esta sección se crea la tabla 'tarea' y se configuran los campos necesarios para el registro de las actividades.
En esta misma sección se instancia al ORM de SqlAlchemy para construir el modelo anteriormente configurado 'tarea'

4. Metodos para el manejo de la tarea

Se crean los metodos necesarios para dar el manejo a un CRUD completo y a otros items adicionales solicitados.

agregar_tarea(POST) = Crea la tarea definiendo unicamente titulo y descripción (solo pide estos items teniendo en cuenta que por defecto se tiene configurada en la base de datos que el boleano de la caracteristica completa por defecto es false)
listar_tareas(GET) = Lista todas las tareas registradas, en caso que no existan tareas enviara el mensaje: (No hay tareas.)
marcar_completada(PUT) = Primero utiliza el metodo listar_tareas para consultar si tenemos tareas disponibles para actualizar y mostrarle al usuario las tareas disponibles. Luego solicita al usuario por medio de un input el Id del item que desea editar para cambiar el estado a completada. Para finalizar cambia el estado de la tarea a completado si el Id cumple con los requerimientos
eliminar_tareas_completadas(DELETE) = Este metodo elimina todas las tareas cuyo estado sea completada.
guardar_tareas(N/A) = Metodo utilizado para almacenar las tareas completadas o no en un archivo .json
cargar_tareas(N/A) = Metodo que nos permite cargar a partir del archivo .json las tareas que contiene el archivo dentro de nuestra base de datos cumpliendo la función de restablecer un backup de mi base de datos.

5. Menu principal

En esta sección se ejecuta lo que simula la interfaz del usuario en la consola de la siguiente manera:

1. Se instancia el metodo principal __main__ este es el metodo principal sobre el cual se inicializara toda nuestra aplicación.
2. Se imprime en pantalla un listado de acciones con un numero que precede la acción, el usuario debera digitar unicamente el numero que referencia la acción para ejecutar el metodo
3. El usuario obtiene el resultado de acuerdo a la logica de operación.



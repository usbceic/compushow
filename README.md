Sistema del CompuShow

=========

REQUISITOS:
	- Django 1.6.2
	- Python 2.7.3
	- Postgresql 9.1.12

¿CÓMO SABER LA VERSIÓN QUE TENGO?

DJANGO
	> python
	Once you’re running python, type:
	>>> import django
	>>> django.get_version()
	>>> exit()

PYTHON
	> python -V

POSTGRESQL
	> psql --version


EJECUCIÓN:
	Crear base de datos en postgresql bajo el nombre compushow, usuario: postgres y contraseña 123456

	Para correr el proyecto:
	1. Abrir el terminal
	2. python manage.py syncdb #Sincroniza la base de datos
	   python manage.py loaddata inscritosEM14.json
	3. python manage.py validate #Verificar si existe algún error en los modelos
	4. python manage.py runserver #Correr el servidor
	5. Abrir explorador
	6. http://127.0.0.1:8000/


DETALLES PARA REALIZARLE AL COMPUSHOW:

FASE NOMINACIÓN:

1. Mensaje de error al subir una foto que no cumpla las condiciones.
2. Mensaje que pudo nominar satisfactoriamente
3. Mensaje de error al filtrar

NOMINACIONES:
CompuMami	
CompuPapi
CompuLove
CompuMaster -> base de datos de los profesores
CompuLolas	
CompuPro
CompuButt	
CompuCartoon
Comadre
Compadre
CompuTuki
CompuCuchi
CompuSelfie***
CompuMicroondas
CompuProductista
CompuChinazo -> escribir chinazo
CompuAdoptado -> se escribe el nombre
CompuTeam -> base de datos de las agrupaciones
CompuChapita
CompuGordito 
CompuCheeseWheez
CompuIntenso
CompuFitness	
CompuSaurio
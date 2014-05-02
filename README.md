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
	Crear base de datos en postgresql bajo el nombre compushow, usuario: postgres y contraseña: 123456

	Para correr el proyecto:
	1. Abrir el terminal y nos dirigimos a la carpeta con el archivo manage.py
	2. python manage.py syncdb #Sincroniza la base de datos
	3. Aceptar la creacion de un usuario
	4. Carga los valores que usaremos para la base de datos
	   python manage.py loaddata inscritosEM14.json
	   python manage.py loaddata profesores.json
	   python manage.py loaddata agrupaciones.json
	   python manage.py loaddata categorias.json
	5. python manage.py validate #Verificar si existe algún error en los modelos
	6. python manage.py runserver #Correr el servidor
	7. Abrir el explorador
	8. http://127.0.0.1:8000/
	
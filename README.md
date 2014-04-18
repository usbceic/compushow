Sistema del CompuShow

=========

DETALLES PARA REALIZARLE AL COMPUSHOW:

FASE NOMINACIÓN:
1. CompuChinazo -> escribir chinazo
2. LOGIN -> el boton de iniciar sesion se active cuando llene ambos cuadros de texto (igual a registrarse).
3. ERROR: Me deja entrar al login aun cuando se esta en etapa cerrada o filtrando.
4. CERRADO -> Mejor idea.
5. NOMINAR -> mensaje exitosamente agregado y widget mostrar fotos.




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
	5. python manage.py validate #Verificar si existe algún error en los modelos
	6. python manage.py runserver #Correr el servidor
	7. Abrir el explorador
	8. http://127.0.0.1:8000/


NOMINACIONES:
CompuMami	
CompuPapi
CompuLove
CompuMaster
CompuLolas	
CompuPro
CompuButt	
CompuCartoon
Comadre
Compadre
CompuTuky
CompuCuchi
CompuSelfie***
CompuMicroondas
CompuProductista
CompuChinazo
CompuAdoptado
CompuTeam
CompuChapita
CompuGordito 
CompuCheeseWhiz
CompuIntenso
CompuFitness	
CompuSaurio
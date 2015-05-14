Repositorio Chile Ayuda

Collaborator



#############################
Software:
-Python 3.4
-Django 1.7.7
#############################
1.- Download last version of the code

2.- Create database
      > python manage.py syncdb

3.- Migrate changes in the database (this step may not be needed in all systems)
      > python manage.py migrate

4.- Load initial data to the database
      > python manage.py loaddata data.json (not implemented yet)

5.- Run the server
   > python manage.py runserver

6.- Now the following URL will take you to the index page
      127.0.0.1:8000/

# Hillel_Django_HW2
Django homework for Hillel IT school. 



# Tasks to do

* In a new repository initialize a new django project with the latest django version
* In the new repository's directory run:

$ django-admin startproject <project-name> .
* Make sure .gitignore escapes database files, virtual environment and .idea folders
* Create requirements.txt (or Pipfile + Pipfile.lock depends on which one is used)
* Create django application 'catalog' and add it into INSTALLED_APPS


$ python manage.py startapp <app_name> 
* Make sure SECRET_KEY is retrieved from environment variables and isn't stored in the repository

os.environ.get("SECRET_KEY", "def value")

* Create README.md in witch describe the project

# Overview

Created new project - 'project_name'

Created app - catalog

requirements.txt was created by command
* $ pip freeze > requirements.txt 

For reading environment variables was used 'python-dotenv' package
* $ pip install python-dotenv

Overall all the tasks has been implemented.

The quality of the implementation will be assessed by the course curator


# Quick start 

Assuming you have Python setup, run the following commands 
(if you're on Windows you may use py or py -3 instead of python to start Python):
* pip3 install -r dev-requirements.txt
* python3 manage.py runserver

Open tab to http://127.0.0.1:8000 to see the main site
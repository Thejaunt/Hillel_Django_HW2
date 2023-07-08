# Hillel_Django_HW2
Django homework for Hillel IT school. 

# Quick start 

Assuming you have Python setup, run the following commands 
(if you're on Windows you may use py or py -3 instead of python to start Python):
* pip3 install -r dev-requirements.txt
* python3 manage.py migrate
* python3 manage.py runserver

Open tab to http://127.0.0.1:8000 to see the main site

# Catalog app
![catalog.png](graph-models%2Fcatalog.png)
* Custom management commands:
  - python3 manage.py create_users {number from 1-10}
  - python3 manage.py delete_users {list of user ids to be deleted} (1 2 5) Except superuser

* Load fixtures
  -  python3 manage.py loaddata fixtures/catalog.json --app catalog
  
In case of UnicodeDecodeError (Windows 11) - open the file; change encoding to utf-8; click on convert option

# Triangle app
![triangle.png](graph-models%2Ftriangle.png)
* Load fixtures
  - python3 manage.py loaddata fixtures/triangle.json --app triangle
  
In case of UnicodeDecodeError (Windows 11) - open the file; change encoding to utf-8; click on convert option

# Bookstore app
![bookstore.png](graph-models%2Fbookstore.png)
* Custom management commands:
  - python3 manage.py create_data
  
will create 100 new entries for each model(Author, Publisher, Book, Store)
  - python3 manage.py create_data --author 1000 --book 500

You can specify amount of entries for each model. But not more than 10_000 entries
  - python3 manage create_data --create_relations 100

Will create relations for 100 randomly chosen from database books
  I'm still working on it. But for now entries are created without relations.
  You can specify amount of already existing in DB books and --create_relations will create rrelations for random book

* Load fixtures
  - python3 manage.py loaddata fixtures/bookstore.json --app bookstore

In case of UnicodeDecodeError (Windows 11) - open  the file; change encoding to utf-8; click on convert option
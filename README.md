# MStackCRM

This is a CRM that aims to be the Wordpress of CRM tools. The end goal would be to better manage customers and get business technology operations going faster

### How to Get Started

1. clone this repo

2. install all the necessary packages (best done inside of a virtual environment)
> pip install -r requirements.txt

3. run the app
> python runserver.py

4. create and seed the db (the server must still be running, so open a new terminal window first)
> python manage.py create_db && python manage.py seed_db --seedfile 'data/db_items.json'

5. check out your blog
> http://localhost:5000/

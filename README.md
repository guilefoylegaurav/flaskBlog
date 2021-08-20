# Flask Blog
## Frontend
Nothing fancy, good old Bootstrap CSS.

## Backend
Used Flask, and sqllite db. Flask-SQLAlchemy provides an ORM for the db. 

## How to Use
Head to the root directory. Create virtual environment. Start Python from command line. Then: 



```
>>> from flask_blog import db
>>> db.create_all()
>>> exit()
```
After that, 

```
>>> python run.py
```
Head to [localhost:5000](https://localhost:5000).



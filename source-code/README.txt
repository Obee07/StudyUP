To create database:
1. Activate virtual environment
2. Go to folder of code
3. Type the following:
>>> python
>>> from studyup import db, create_app
>>> app=create_app()
>>> ctx=app.app_context()
>>> ctx.push()
>>> //database queries here like db.create_all() etc.
>>> ctx.pop()
>>> exit()

To run app:
1. Activate virtual environment
2. Go to folder of code (directory must look like "..\code>")
3. Type the following:
>>> python run.py
4. Open a web browser and type in 'localhost:5000'

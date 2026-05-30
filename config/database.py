import mysql.connector

def get_db():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="kitten8184",
        database="recipe_app"
    )
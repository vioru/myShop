from flask_app.config.mysqlconnection import  connectToMySQL
from flask import flash

class Favorite:
    def __init__(self,data):
        self.users_id = data['users_id']
        self.Products_id = data['Products_id']
    
    
    @classmethod
    def save_fav(cls, formulario):
        query = "INSERT INTO favs (user_id,product_id) VALUES ( %(user_id)s, %(product_id)s)"
        newfav = connectToMySQL('mytienda').query_db(query, formulario)

        return newfav
    
    @classmethod
    def consult_fav(cls,formulario):
        query = "SELECT * FROM favs WHERE user_id =  %(user_id)s AND product_id = %(product_id)s "
        result = connectToMySQL('mytienda').query_db(query, formulario)
        return result

    @classmethod
    def update_fav(cls, formulario): 
        query = "UPDATE favs SET on_off = 0, WHERE user_id =  %(user_id)s"
        result = connectToMySQL('mytienda').query_db(query, formulario)
        return result



    
    @classmethod
    def delete_fav(cls, formulario): 
        query = "DELETE FROM favs WHERE user_id = %(user_id)s  AND product_id = %(product_id)s "
        result = connectToMySQL('mytienda').query_db(query, formulario)
        return result
    
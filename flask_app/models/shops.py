from flask_app.config.mysqlconnection import  connectToMySQL
from flask import flash
from flask_app.models.products import Product
import re
from werkzeug.utils import secure_filename
import os 

ALLOWED_EXTENSIONS = set(["png","jpg","jpeg"])

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=\w*[0-9])(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')
list_products=[]

class Shop:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email_shop = data['email_shop']
        self.password = data['password']
        self.category = data['category']
        self.description_shop = data['description_shop']
        self.color = data['color'] 
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        self.logo_img = data['logo_img'] 


    @staticmethod
    def valid_shop(formulario):
        es_valido = True

        if len(formulario['name']) < 3:        
            flash("El nombre de la nueva tarea debe tener al menos 3 caracteres", 'registershop')
            es_valido = False
        
        
        if not EMAIL_REGEX.match(formulario['email_shop']):
            flash('Email inválido', 'registershop')
            es_valido = False
        

        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas no coinciden', 'registershop')
            es_valido = False
        

        if not PASSWORD_REGEX.match(formulario['password']):
            flash('Contraseña inválida, la contraseña debe tener al entre 8 y 16 caracteres, al menos un número, al menos una minúscula y al menos una mayúscula, no puede tener otros símbolos.', 'registershop')
            es_valido = False
        
        
        query = "SELECT * FROM shops WHERE email_shop= %(email_shop)s"
        results = connectToMySQL('mytienda').query_db(query,formulario)
        if len(results) >= 1 :
            flash(' este E-mail ya esta registrado','registershop')
            es_valido = False
        

        if formulario['category'] == str(0):
            flash("Escoge una categoria", 'registershop')
            es_valido = False
            
        if len(formulario['description_shop']) < 5:
            flash("La descripcion debe tener al menos 5 caracteres", 'registershop')
            es_valido = False

        if len(formulario['description_shop']) == "":
            flash("Debes agregar una descripción", 'registershop')
            es_valido = False
        
        return es_valido 
    


    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO shops(name, email_shop , password , category,description_shop, color ) VALUES (%(name)s, %(email_shop)s,%(password)s, %(category)s, %(description_shop)s, %(color)s)"
        result = connectToMySQL('mytienda').query_db(query, formulario) 
        return result 
    
    @classmethod
    def show_shops(cls): #   " SELECT *FROM mytienda.shops  LEFT JOIN products ON shops.id = products.shop_id "
        query = "SELECT * FROM mytienda.shops "
        results = connectToMySQL('mytienda').query_db(query)
        
        shops = []
        for s in results:
            instancia_tienda = cls(s)
            formulario = {"id": instancia_tienda.id, "user_id" : 0}
            instancia_tienda.list_products= Product.get_products_shops(formulario)
            shops.append(instancia_tienda)
        return shops
    

    @classmethod
    def show_shops_category(cls,formulario):#"SELECT * FROM mytienda.shops LEFT JOIN products ON shops.id = products.shop_id WHERE category = %(category)s"
        query ="SELECT * FROM mytienda.shops WHERE category = %(category)s"
        results = connectToMySQL('mytienda').query_db(query,formulario)
        
        shops = []
        for s in results:
            instancia_tienda = cls(s)
            formulario = {"id": instancia_tienda.id, "user_id" : 0}
            instancia_tienda.list_products= Product.get_products_shops(formulario)
            shops.append(instancia_tienda)
        return shops
    



    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM shops WHERE id = %(id)s"
        result = connectToMySQL('mytienda').query_db(query, formulario) 
        shop = cls(result[0])
        
        return shop
    
    @classmethod
    def get_by_email_shop(cls, formulario):
        query = "SELECT * FROM shops WHERE email_shop = %(email)s"
        result = connectToMySQL('mytienda').query_db(query, formulario)
        if len(result) < 1:
            return False
        else:
            shop = cls(result[0]) 
            return shop

    @classmethod
    def update_logo(cls, formulario): 
        query = "UPDATE shops SET logo_img = %(logo_img)s WHERE id = %(id)s"
        result = connectToMySQL('mytienda').query_db(query, formulario)
        return result
    
    @classmethod
    def delete_shop(cls, formulario): 
        query = "DELETE FROM shops WHERE id = %(id)s"
        result = connectToMySQL('mytienda').query_db(query, formulario)
        return result
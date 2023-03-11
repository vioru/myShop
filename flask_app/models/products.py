from flask_app.config.mysqlconnection import  connectToMySQL
from flask import flash
import re

URL_REGEX = re.compile (r'^https?:\/\/.*\.(?:png|jpg)$')





class Product:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description_pro = data['description_pro']
        self.price = data['price']
        self.status = data['status']
        self.img = data['img']
        self.shop_id = data['shop_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']  

        
        self.is_fav = data['is_fav']
    


    @staticmethod
    def valid_product(formulario):
        es_valido = True

        if len(formulario['name']) < 3:
            flash("El nombre debe tener al menos 3 caracteres", "product")
            es_valido = False
        
        if len(formulario['description_pro']) < 5:
            flash("La descripcion debe tener al menos 5 caracteres", "product")
            es_valido = False

        if len(formulario['description_pro']) == "":
            flash("Debes agregar una descripción", "product")
            es_valido = False

        if formulario['price'] == "":
            flash("debe ingresar un valor al producto", "product")
            es_valido = False
        
        if formulario['price'] == str:
            flash("debe ingresar un numero", "product")
            es_valido = False

        if formulario['status'] == str(0):
            flash("debe escoger un estado", "product")
            es_valido = False

        
        if not URL_REGEX.match(formulario['img']):
            flash('Url invalida, debe ser una url de imagen png o jpg', 'product')
            es_valido = False
        return es_valido  

    @classmethod
    def save_product(cls, formulario):
        query = "INSERT INTO products(name, description_pro, price, status, img, shop_id) VALUES (%(name)s, %(description_pro)s, %(price)s, %(status)s,%(img)s, %(shop_id)s)"
        result = connectToMySQL('mytienda').query_db(query, formulario) 
        return result 

    @classmethod   #SELECT * FROM mytienda.products  LEFT JOIN favs ON products.id = favs.Products_id WHERE shop_id = %(id)s"
    def get_all_products (cls):
        query = "SELECT * FROM products "
        results = connectToMySQL('mytienda').query_db(query) 
        products = []
        
        for e in results:
            products.append(cls(e)) 
        return products

    @classmethod   #SELECT * FROM mytienda.products  LEFT JOIN favs ON products.id = favs.Products_id WHERE shop_id = %(id)s"
    def get_products_shops(cls, formulario):
        query = "SELECT *,CASE WHEN favs.user_id IS NULL THEN 0 ELSE 1 END is_fav FROM mytienda.products  left JOIN favs ON products.id = favs.Product_id AND favs.user_id= %(user_id)s WHERE shop_id = %(id)s"
        results = connectToMySQL('mytienda').query_db(query,formulario) 
        products = []
        
        for e in results:
            products.append(cls(e)) 
        return products
    

    @classmethod
    def favorites_by_user(cls,formulario):
        query = "SELECT * ,CASE WHEN favs.user_id IS NULL THEN 0 ELSE 1 END is_fav  FROM mytienda.products  left JOIN favs ON products.id = favs.Product_id  WHERE favs.user_id = %(id)s"
        results = connectToMySQL('mytienda').query_db(query,formulario) 
        favorites = []
        
        for e in results:
            favorites.append(cls(e)) 
        return favorites


    @classmethod
    def get_products_user(cls,formulario): 
        query = "SELECT products.*  FROM products WHERE user_id = %(id)s"
        results = connectToMySQL('mytienda').query_db(query,formulario) 
        products = []
        
        for e in results:
            
            products.append(cls(e)) 
        return products


    @classmethod
    def get_by_id(cls, formulario): 
        query = "SELECT products.*,0 is_fav FROM products WHERE id = %(id)s"
        result = connectToMySQL('mytienda').query_db(query, formulario) 
        product = cls(result[0])
        return product

    @classmethod
    def update_product(cls, formulario): 
        query = "UPDATE products SET name = %(name)s, description_pro = %(description_pro)s, status = %(status)s ,price = %(price)s , img = %(img)s WHERE id = %(product_id)s"
        result = connectToMySQL('mytienda').query_db(query, formulario)
        return result
    

    @classmethod
    def delete_product(cls, formulario): 
        query = "DELETE FROM products WHERE id = %(id)s"
        result = connectToMySQL('mytienda').query_db(query, formulario)
        return result
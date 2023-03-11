from flask_app.config.mysqlconnection import  connectToMySQL
from flask import flash

import re

URL_REGEX = re.compile (r'^https?:\/\/.*\.(?:png|jpg)$')

class Proposal:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description_pro = data['description_pro']
        self.img = data['img']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.shop_id = data['shop_id']
        self.user_id = data['user_id']
    
    @staticmethod
    def valid_proposal(formulario):
        es_valido = True

        if len(formulario['name']) < 3:
            flash("El nombre debe tener al menos 3 caracteres", "proposal")
            es_valido = False
        
        if len(formulario['description_pro']) < 5:
            flash("La descripcion debe tener al menos 5 caracteres", "proposal")
            es_valido = False

        if len(formulario['description_pro']) == "":
            flash("Debes agregar una descripción", "proposal")
            es_valido = False
        
        if not URL_REGEX.match(formulario['img']):
            flash('Url invalida, debe ser una url de imagen png o jpg', 'proposal')
            es_valido = False
            
        return es_valido  
    
    @classmethod
    def save_proposal(cls, formulario):
        query = "INSERT INTO proposal (name, description_pro, img, shop_id, user_id) VALUES (%(name)s, %(description_pro)s, %(img)s,%(shop_id)s ,%(user_id)s)"
        result = connectToMySQL('mytienda').query_db(query, formulario) 
        return result 
    
    
    @classmethod
    def view_proposal_ShopId(cls, formulario):
        query = "SELECT * FROM proposal WHERE shop_id = %(id)s"
        results = connectToMySQL('mytienda').query_db(query,formulario) 
        proposals = []
        
        for e in results:
            proposals.append(cls(e)) 
        return proposals

    @classmethod
    def view_proposal_userid(cls, formulario):
        query = "SELECT * FROM proposal WHERE user_id = %(id)s"
        results = connectToMySQL('mytienda').query_db(query,formulario) 
        proposals = []
        
        for e in results:
            proposals.append(cls(e)) 
        return proposals

    
    @classmethod
    def delete_product(cls, formulario): 
        query = "DELETE FROM products WHERE id = %(id)s"
        result = connectToMySQL('mytienda').query_db(query, formulario)
        return result

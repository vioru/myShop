from flask_app.config.mysqlconnection import  connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=\w*[0-9])(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')



class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.profile_img = data['profile_img']
        self.direction = data['direction']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']    


    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users(first_name, last_name, email, password , direction ) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(direction)s)"
        result = connectToMySQL('mytienda').query_db(query, formulario) 
        return result 
    
    @staticmethod
    def valida_usuario(formulario):
        
        es_valido = True

        if len(formulario['first_name'])< 3 :
            flash ('Tu nombre debe tener al menos 3 caracteres', 'registeruser')
            es_valido = False
        
        if len(formulario['last_name'])< 3 :
            flash('Tu Apellido debe tener al menos 3 caracteres', 'registeruser')
            es_valido = False
        
        if not EMAIL_REGEX.match(formulario['email']):
            flash('Email inválido', 'registeruser')
            es_valido = False
        
        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas no coinciden', 'registeruser')
            es_valido = False
        
        if not PASSWORD_REGEX.match(formulario['password']):
            flash('Contraseña inválida, la contraseña debe tener al entre 8 y 16 caracteres, al menos un número, al menos una minúscula y al menos una mayúscula, no puede tener otros símbolos.', 'registeruser')
            es_valido = False

        query = "SELECT * FROM users WHERE email= %(email)s"
        results = connectToMySQL('login_reg').query_db(query,formulario)
        if len(results) >= 1 :
            flash(' este E-mail ya esta registrado','registeruser')
            es_valido = False
        
        if len(formulario['direction'])< 3 :
            flash ('Tu dirección debe tener al menos 3 caracteres', 'registeruser')
            es_valido = False
        

        return es_valido
    
    @classmethod
    def get_by_email(cls, formulario):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('mytienda').query_db(query, formulario)
        if len(result) < 1:
            return False
        else:
            
            user = cls(result[0]) 
            return user

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('mytienda').query_db(query, formulario) 
        user = cls(result[0])
        
        return user


    @classmethod
    def update_logouser(cls, formulario): 
        query = "UPDATE users SET profile_img = %(profile_img)s WHERE id = %(id)s"
        result = connectToMySQL('mytienda').query_db(query, formulario)
        return result


    @classmethod
    def delete_user(cls, formulario): 
        query = "DELETE FROM users WHERE id = %(id)s"
        result = connectToMySQL('mytienda').query_db(query, formulario)
        return result
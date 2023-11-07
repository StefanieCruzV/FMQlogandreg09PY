from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
NAME =re.compile(r'^[a-zA-Z ]+$' )
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Login:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email= data['email']
        self.password= data['password']
      
    # Now we use class methods to query our database

    @classmethod
    def save(cls, data):
        query = "INSERT INTO login ( first_name , last_name , email , password ) VALUES ( %(first_name)s , %(last_name)s , %(email)s  , %(password)s)"
        # los nombres deben ser los de la bd / los valores los del html
        return connectToMySQL('login').query_db(query, data)
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM login WHERE email = %(email)s;"
        results = connectToMySQL("login").query_db(query,data)
        # Didn't find a matching user
        if len(results) < 1: #Si me devuelve algun row, el arreglo va a tener este row de la DB
            return False
        return cls(results[0]) # crea un objecto/instancia de la clase Login

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not NAME.match(user['first_name']):
            flash("Name must be only characters.")
            is_valid = False
        if  len(user['first_name']) < 2:
            flash("Name must be at least 2 .")
            is_valid = False
        if not NAME.match(user['last_name']):
            flash("Last name must be only characters.")
            is_valid = False
        if  len(user['first_name']) < 2:
            flash("Last ame must be at least 2 .")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 8 :
            flash("Password must be at least 8 characters.")
            is_valid = False
        if len(user['con_password']) == 0:
            flash("must ned the confirmation")
            is_valid = False
        if user['password'] != user['con_password']:
            flash("Confirmation must match the password")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(form):
        is_valid = True
        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(form['password']) < 8 :
            flash("Password must be at least 8 characters.")
            is_valid = False
        return is_valid





    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM users;"

    #     results = connectToMySQL('usersHw').query_db(query)
    #     # guarda el resultado de la bd
        
    #     users = []
    #     # crea arreglo para guiardar los valores 
    #     for user in results: #itera los nombres de la base de datos 
    #         users.append(cls(user))
    #         # flos mete en el arreglo -y los convierte en una clkase ususario
    #     return users

    # @classmethod
    # def delete(cls, data):
    #     query = "DELETE FROM users WHERE id = %(id)s"
    #     connectToMySQL('usersHw').query_db(query, data)
    #     return 

    # @classmethod
    # def get_user_by_id(cls, data):
    #     query = "SELECT * FROM users WHERE id = %(id)s"
    #     # los nombres deben ser los de la bd / los valores los del html
    #     result= connectToMySQL('usersHw').query_db(query, data)
    #     single_user= cls(result[0]) 
    #     return single_user

    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE users SET first_name = %(uname)s , last_name = %(ulastname)s , email= %(uemail)s , created_at = NOW(), updated_at= NOW() WHERE id= %(id)s;"
    #     # los nombres deben ser los de la bd / los valores los del html
    #     return connectToMySQL('usersHw').query_db(query, data)



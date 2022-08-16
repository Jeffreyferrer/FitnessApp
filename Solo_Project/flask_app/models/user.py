from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
import re
EMAILREGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile('^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')
db_name = 'my_fitness'
bcrypt = Bcrypt(app)

class User:
    

    def __init__(self,data): 
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"   
        return connectToMySQL(db_name).query_db(query, data)
        


    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db_name).query_db(query)
        users= []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod 
    def get_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db_name).query_db(query, data)
        if not results:
            return results
        else:
            return cls(results[0])

    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s"
        results = connectToMySQL(db_name).query_db(query, data)
        if not results:
            return False
        else:
            return cls(results[0])

    @staticmethod
    def validate_register(data):
        is_valid = True 
        if not EMAILREGEX.match(data['email']):
            flash('email must contain a period and @ sign')
            is_valid= False
        
        email_data= {'email': data['email']}
        user = User.get_email(email_data)
        if user:
            flash('This email already exist')
            is_valid = False
        
        if not data['first_name'].isalpha():
            flash('First Name Requires letters')
            is_valid = False
        if not data['last_name'].isalpha():
            flash('Last Name Requires letters')
            is_valid = False
        if len(data['first_name']) < 2:
            flash('First Name must be at least 2 characters')
            is_valid = False
        if len(data['last_name']) < 2: 
            flash('Last Name must be at least 2 characters')
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash('Password must be between 8-20 characters')
            flash('Password must include a number')
            flash('Password must include one upper and lower case character')
            flash('Password must include a special character')
            is_valid = False
        
        if not data['password'] == data['confirm_password']:
            flash('Passwords Must Match')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid= True
        email_data= {'email': data['email']}
        user = User.get_email(email_data)
        if not user:
            flash('Invalid email','login')
            is_valid= False
        elif not bcrypt.check_password_hash(user.password, data['password']):
            flash('Invalid password''login')
            is_valid= False
        
        return is_valid
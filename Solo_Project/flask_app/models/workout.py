from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

db_name = 'my_fitness'

class Workout:
    

    def __init__(self, data):
        self.id = data['id']
        self.exercise = data['exercise'] 
        self.sets = data['sets'] 
        self.reps = data['reps'] 
        self.weight = data['weight'] 
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def read_all(cls):
        query = "SELECT * FROM workouts;"  
        results = connectToMySQL(db_name).query_db(query)
        all_workouts = []
        for row in results:
            all_workouts.append(cls(row))
        return all_workouts

    @classmethod
    def create(cls, data):
        query = "INSERT INTO workouts (exercise, sets, reps, weight, user_id) VALUES (%(exercise)s, %(sets)s, %(reps)s, %(weight)s, %(user_id)s);"
        results = connectToMySQL(db_name).query_db(query, data)
        return results

    @classmethod
    def read_id(cls, data):
        query = "SELECT * FROM workouts WHERE id=%(id)s;"
        results = connectToMySQL(db_name).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE workouts SET exercise=%(exercise)s, sets=%(sets)s, reps=%(reps)s, weight=%(weight)s, user_id=%(user_id)s, updated_at=NOW() WHERE id=%(id)s"
        return connectToMySQL(db_name).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM workouts WHERE id=%(id)s"
        return connectToMySQL(db_name).query_db(query, data)
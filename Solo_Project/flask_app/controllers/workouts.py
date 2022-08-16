from flask_app import app
from flask import render_template, redirect, flash, session, request 
from flask_app.models.workout import Workout

@app.route("/workouts/new")
def new_workout():
    return render_template("new_workout.html")


@app.route("/workouts/create", methods=["POST"])
def create_workout():
    data = {
        "exercise": request.form['exercise'],
        "sets": request.form['sets'],
        "reps": request.form['reps'],
        "weight": request.form['weight'],
        "user_id": session['user_id']
    }
    Workout.create(data)
    return redirect("/chest")

@app.route("/workouts/edit/<int:id>")
def edit_workout(id):
    workout_to_edit = Workout.read_id({"id":id}) #user editing workout
    return render_template("edit_workout.html", workout = workout_to_edit)

@app.route("/workouts/update", methods=["POST"])
def update_workout():
    data = {
        "id": request.form['id'],
        "exercise": request.form['exercise'],
        "sets": request.form['sets'],
        "reps": request.form['reps'],
        "weight": request.form['weight'],
        "user_id": request.form['user_id']
    }
    # print(data) #checking if something went wrong with my code
    Workout.update(data)
    return redirect("/chest")


@app.route("/workouts/delete/<int:id>")
def delete_workout(id):
    data = {
        "id": id
    }
    Workout.delete(data) 
    return redirect("/chest")

@app.route("/workouts/<int:id>")
def view_workout(id):
    workout_to_edit = Workout.read_id({"id":id})
    return render_template("view_workout.html", workout = workout_to_edit)
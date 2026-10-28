from flask import Flask, request, make_response
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercise

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db, render_as_batch=True)

db.init_app(app)




@app.route('/workouts', methods=['GET'])
def get_workouts():
    return {'message': 'GET /workouts not built yet'}, 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    return {'message': f'GET /workouts/{id} not built yet'}, 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    return {'message': 'POST /workouts not built yet'}, 200


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    return {'message': f'DELETE /workouts/{id} not built yet'}, 200




@app.route('/exercises', methods=['GET'])
def get_exercises():
    return {'message': 'GET /exercises not built yet'}, 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    return {'message': f'GET /exercises/{id} not built yet'}, 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    return {'message': 'POST /exercises not built yet'}, 200


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    return {'message': f'DELETE /exercises/{id} not built yet'}, 200




@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    return {'message': 'POST workout_exercises not built yet'}, 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
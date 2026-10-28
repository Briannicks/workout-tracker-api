from flask import Flask, request, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db, render_as_batch=True)

db.init_app(app)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=('workout_exercises',))
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=('workout_exercises',))
workout_exercise_schema = WorkoutExerciseSchema()


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return {'error': f'Workout {id} not found'}, 404
    return workout_schema.dump(workout), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
    except ValidationError as e:
        return {'errors': e.messages}, 400
    except ValueError as e:
        return {'error': str(e)}, 400
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Workout could not be saved: invalid data.'}, 400

    return workout_schema.dump(workout), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return {'error': f'Workout {id} not found'}, 404

    db.session.delete(workout)
    db.session.commit()
    return make_response('', 204)


@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return {'error': f'Exercise {id} not found'}, 404
    return exercise_schema.dump(exercise), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
    except ValidationError as e:
        return {'errors': e.messages}, 400
    except ValueError as e:
        return {'error': str(e)}, 400
    except IntegrityError:
        db.session.rollback()
        return {'error': 'An exercise with that name already exists.'}, 400

    return exercise_schema.dump(exercise), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return {'error': f'Exercise {id} not found'}, 404

    db.session.delete(exercise)
    db.session.commit()
    return make_response('', 204)


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return {'error': f'Workout {workout_id} not found'}, 404

    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return {'error': f'Exercise {exercise_id} not found'}, 404

    try:
        data = workout_exercise_schema.load(request.get_json(silent=True) or {})
        workout_exercise = WorkoutExercise(workout=workout, exercise=exercise, **data)
        db.session.add(workout_exercise)
        db.session.commit()
    except ValidationError as e:
        return {'errors': e.messages}, 400
    except ValueError as e:
        return {'error': str(e)}, 400
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Could not add exercise to workout: invalid data.'}, 400

    return workout_exercise_schema.dump(workout_exercise), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
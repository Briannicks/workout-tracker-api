#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Clearing old data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Creating exercises...")
    squat = Exercise(name="Squat", category="strength", equipment_needed=False)
    bench_press = Exercise(name="Bench Press", category="strength", equipment_needed=True)
    deadlift = Exercise(name="Deadlift", category="strength", equipment_needed=True)
    running = Exercise(name="Running", category="cardio", equipment_needed=False)
    plank = Exercise(name="Plank", category="balance", equipment_needed=False)
    hamstring_stretch = Exercise(name="Hamstring Stretch", category="flexibility", equipment_needed=False)
    db.session.add_all([squat, bench_press, deadlift, running, plank, hamstring_stretch])

    print("Creating workouts...")
    leg_day = Workout(date=date(2026, 10, 20), duration_minutes=60, notes="Leg day, focus on form.")
    upper_body = Workout(date=date(2026, 10, 22), duration_minutes=45, notes="Upper body strength.")
    cardio_day = Workout(date=date(2026, 10, 24), duration_minutes=30, notes="Light cardio and core.")
    db.session.add_all([leg_day, upper_body, cardio_day])

    print("Adding exercises to workouts...")
    db.session.add_all([
        WorkoutExercise(workout=leg_day, exercise=squat, reps=10, sets=4),
        WorkoutExercise(workout=leg_day, exercise=deadlift, reps=8, sets=3),
        WorkoutExercise(workout=leg_day, exercise=hamstring_stretch, duration_seconds=60),
        WorkoutExercise(workout=upper_body, exercise=bench_press, reps=10, sets=3),
        WorkoutExercise(workout=upper_body, exercise=plank, duration_seconds=90),
        WorkoutExercise(workout=cardio_day, exercise=running, duration_seconds=1200),
        WorkoutExercise(workout=cardio_day, exercise=plank, duration_seconds=60),
    ])

    db.session.commit()
    print("Done seeding!")
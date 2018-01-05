def get_collection_exercise_by_period(exercises, period):
    for exercise in exercises:
        if exercise['name'] == period:
            return exercise

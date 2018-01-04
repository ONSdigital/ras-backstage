def filter_collection_exercises(exercises, period):
    for exercise in exercises:
        if exercise['name'] == period:
            return exercise
    return None

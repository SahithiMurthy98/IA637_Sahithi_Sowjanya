from baseObject import baseObject


class workout(baseObject):
    def __init__(self):
        super().__init__()
        self.setup()

    def get_all_workouts(self):
        self.getAll()
        return self.data

    def get_workout_by_id(self, pkval):
        self.getById(pkval)
        if self.data:
            return self.data[0]
        else:
            return None  # Return None if no data found


    def add_workout(self, workoutname, category):
        d = {'workoutname': workoutname, 'category': category}
        self.set(d)
        self.insert()
        return True

    def update_workout(self, pkval, workoutname, category):
        self.getById(pkval)
        if self.data:
            self.data[0]['workoutname'] = workoutname
            self.data[0]['category'] = category
            self.update()
            return True
        return False

    def delete_workout(self, pkval):
        self.deleteById(pkval)
        return True



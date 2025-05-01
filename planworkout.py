from baseObject import baseObject

class planworkout(baseObject):
    def __init__(self):
        super().__init__()
        self.setup()

    def add_workout_to_plan(self, planid, workoutid):
        d = {'planid': planid, 'workoutid': workoutid}
        self.set(d)
        self.insert()
        return True

    def get_workouts_by_plan(self, planid):
        sql = f"SELECT w.* FROM workouts w JOIN planworkouts pw ON w.workoutid = pw.workoutid WHERE pw.planid = %s"
        self.cur.execute(sql, (planid,))
        self.data = [row for row in self.cur]
        return self.data

    def remove_workout_from_plan(self, planid, workoutid):
        sql = "DELETE FROM planworkouts WHERE planid = %s AND workoutid = %s"
        self.cur.execute(sql, (planid, workoutid))
        self.conn.commit()
        return True

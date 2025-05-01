from baseObject import baseObject
import datetime

class activityLog(baseObject):
    def __init__(self):
        super().__init__()
        self.setup()

    def start_workout(self, userid, workoutid):
        d = {
            'userid': userid,
            'workoutid': workoutid,
            'planid': None,
            'starttime': datetime.datetime.now(),
            'endtime': None
        }
        self.set(d)
        self.insert()
        return self.data[0][self.pk]  # Return generated activityid

    def start_plan(self, userid, planid):
        d = {
            'userid': userid,
            'workoutid': None,
            'planid': planid,
            'starttime': datetime.datetime.now(),
            'endtime': None
        }
        self.set(d)
        self.insert()
        return self.data[0][self.pk]  # Return generated activityid

    def end_activity(self, activityid):
        self.getById(activityid)
        if self.data:
            self.data[0]['endtime'] = datetime.datetime.now()
            self.update()
            return True
        return False

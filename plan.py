from baseObject import baseObject


class plan(baseObject):
    def __init__(self):
        super().__init__()
        self.setup()

    def get_all_plans(self):
        self.getAll()
        return self.data

    def get_plan_by_id(self, pkval):
        self.getById(pkval)
        return self.data[0] if self.data else None

    def add_plan(self, planname):
        d = {'planname': planname, 'status': None}  # NULL initially
        self.set(d)
        self.insert()
        return True

    def update_plan(self, pkval, planname):
        self.getById(pkval)
        if self.data:
            self.data[0]['planname'] = planname
            self.update()
            return True
        return False

    def delete_plan(self, pkval):
        self.deleteById(pkval)
        return True

    def start_plan(self, planid):
        self.getById(planid)
        if self.data and (self.data[0]['status'] is None or self.data[0]['status'] == ''):
            self.data[0]['status'] = 'Active'
            self.update()
            return True
        return False

    def complete_plan(self, planid):
        self.getById(planid)
        if self.data and self.data[0]['status'] == 'Active':
            self.data[0]['status'] = 'Completed'
            self.update()
            return True
        return False



class TaskInit:

    def __init__(self, task_id, pending_length=None):
        self.task_id = task_id
        self.pending_length = pending_length

    @property
    def task_id_attr(self):
        return self.task_id

    @task_id_attr.setter
    def task_id_attr(self, task_id):
        self.task_id = task_id

    @property
    def pending_length_attr(self):
        return self.pending_length

    @pending_length_attr.setter
    def pending_length_attr(self, pending_length):
        self.pending_length = pending_length
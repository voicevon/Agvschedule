
TASK_STATE = {"NoPlan":1, "Planed":2, "MovingToSouce":3}

class Task:
    def __init__(self, task_id:int) -> None:
        self.States = {"NoPlan":1, "Planed":2, "MovingToSouce":3}
        self.State = self.States["NoPlan"]
        self.task_id = task_id
        self.SourceStation_id = 0
        self.TargetStation_id = 0
        self.AgvBot = None
    

    
class TaskQueue():
    tasks = []
    
    def __init__(self) -> None:
        pass

    @classmethod
    def FetchSingleTask(cls) -> Task:
        for task in cls.tasks:
            if task.State == TASK_STATE["NoPlan"]:
                return task
        return None

    @classmethod
    def AppendTask(cls, task_id:int, source_station:int, target_station:int)->bool:
        task = Task(task_id)
        task.SourceStation_id = source_station
        task.TargetStation_id = target_station
        cls.tasks.append(task)

    @classmethod
    def __str__(cls):
        return 'tasks len() =' + str(cls.tasks.__len__())

    __repr__ = __str__
    show = __str__
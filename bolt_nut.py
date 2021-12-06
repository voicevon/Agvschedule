
class WorkStation:
    def __init__(self) -> None:
        pass


class AgvBot:
    def __init__(self, bot_id) -> None:
        self.States = ["Idle", "MovingToSource", "Loading","MovingToTarget","OffLoading"]
        self.id = bot_id
        self.State = "Idle"
        self.current_point = 0
        self.current_task: Task
        self.path_to_source = []
        self.path_to_target = []


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
    def __init__(self) -> None:
        self.tasks = []

    def FetchSingleTask(self) -> Task:
        for task in self.tasks:
            if task.State == TASK_STATE["NoPlan"]:
                return task
        return None

    def AppendTask(self, task_id:int, source_station:int, target_station:int)->bool:
        task = Task(task_id)
        task.SourceStation_id = source_station
        task.TargetStation_id = target_station


class AgvBotQueue():
    def __init__(self, total_agv_count = 3) -> None:
        for i in range(total_agv_count):
            new_bot = AgvBot(i)
            self.agvbots.append(new_bot)

    def FetchSingleAGV(self) -> AgvBot:
        '''
        This can be very complex!
        '''
        for bot in self.agvbots:
            if bot.State == 'Idle':
                return bot
        # All agv bots are busy
        return None

    def GetBotFromId(self, bot_id:int) -> AgvBot:
        return None

    def UpdateAgvState(self, id: int, current_point: int, state: str) -> None:
        '''
        This function is a callback of MQTT subscription.
        '''
        bot = self.GetBotFromId(id)
        bot.current_point = current_point
        bot.State = state


class CommuUpper():
    def __init__(self) -> None:
        pass

    def SpinOnce():
        '''
        Access API to find new task
        '''
        if True:

            task_id = 1
            source_station = 2
            target_station = 3
            TaskQueue.AppendTask(task_id, source_station, target_station)
            # Update server
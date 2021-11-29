




import time


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


class Task:
    def __init__(self) -> None:
        self.States = {"NoPlan":1, "Planed":2, "MovingToSouce":3}
        self.State = self.States["NoPlan"]
        self.SourceStation_id = 0
        self.TargetStation_id = 0
        self.AgvBot = None
    

class AgvScheduler:
    '''
    
    '''

    def __init__(self) -> None:
        self.tasks = []
        self.agvbots = []
        for i in range(3):
            new_bot = AgvBot(i)
            self.agvbots.append(new_bot)

        self.track_nodes_count = 8
            


    def AppendTask(self, new_task:Task):
        self.tasks.append(new_task)

    def GetNoPlanTask(self) -> Task:
        for task in self.tasks:
            if task.State = "NoPlan":
                return task
        return None

    def GetAgvBot_on_idle(self) -> AgvBot:
        '''
        This can be very complex!
        '''
        for bot in self.agvbots:
            if bot.State == 'Idle':
                return bot
        # All agv bots are busy
        return None


    def GetTrackPath(self, start_point, end_point) -> list:
        path = []
        point = start_point
        if start_point > end_point:
            end_point += self.track_nodes_count
        while point < end_point:
            point += 1
            path.append(point % self.track_nodes_count)
        return path

    def Plan(self, task: Task, bot: AgvBot):
        task.AgvBot = bot
        # calculate path to source point
        bot.path_to_source = self.GetTrackPath(bot.current_point, task.SourceStation_id)
        # calculate path to target point
        bot.path_to_target = self.GetTrackPath(bot.path_to_source,task.TargetStation_id)

        # Update path plan to MQTT
        task.State = Task.States["Planed"]

    def GetBotFromId(self, bot_id:int) -> AgvBot:
        return None

    def UpdateAgvState(self, id: int, current_point: int, state: str) -> None:
        '''
        This function is a callback of MQTT subscription.
        '''
        bot = self.GetBotFromId(id)
        bot.current_point = current_point
        bot.State = state

    def SpinOnce(self) -> None:
        '''
        '''
        # deal task
        task = self.GetNoPlanTask()
        if task != None:
            agv = self.GetAgvBot_on_idle()
            if agv != None:
                self.Plan(task,agv)


if __name__ == '__MAIN__':
    myScheduler = AgvScheduler()
    while True:
        myScheduler.SpinOnce()
        time.sleep(0.1)



import time

from bolt_nut import AgvBotAgent, AgvBotAgent, AgvBotQueue
from task_queue import Task, TaskQueue

class PathMap：
    '''
    This is a 2D map.   Stations are sit on.
    Will help to find a path from Station-A to Station-B
    1. Points Can be identified by RFid reader. or QR-code reader.
    2. Track might be spilited in from of a Point.
    '''
    def __init__(self) -> None:
        pass


class AgvScheduler:
    '''
    To upper lever users:
        AppendTask(pickup_from_staion, dropbox_to_station)

    '''
    track_nodes_count = 8
    def __init__(self) -> None:
        pass

    @staticmethod
    def AppendTask(pickup_from_staion, dropbox_to_station):
        pass

    @classmethod            
    def GetTrackPath(cls, start_point, end_point) -> list:
        '''
        Core function of the system.
        Mainly will do:
            1. Select an AGV, This has been done before invoking me.
            This function will do:
            2. Calculate Path-A: from current position to source station which is in the task.
            3. Calculate Path-B: from source staion to target station.
        Idea:
            1. Read the map, Append points to the target path

        '''
        path = []
        point = start_point
        if start_point > end_point:
            end_point += cls.track_nodes_count
        while point < end_point:
            point += 1
            path.append(point % cls.track_nodes_count)
        return path

    @classmethod
    def Plan(cls, task: Task, bot:AgvBotAgent) -> bool:
        '''
        Core function of the system.
        Mainly will do:
            1. Select an AGV, This has been done before invoking me.
            2. Calculate Path-A: from current position to source station which is in the task.
            3. Calculate Path-B: from source staion to target station.
        '''
        task.AgvBot = bot
        # calculate path to source point
        path_to_source = cls.GetTrackPath(bot.current_point, task.SourceStation_id)
        # calculate path to target point
        path_to_target = cls.GetTrackPath(bot.path_to_source,task.TargetStation_id)
        bot.StartTask(path_to_source, path_to_target)


    @classmethod
    def SpinOnce(cls) -> None:
        '''
        Core function of the system.
        Mainly will do:
            1. Select an AGV
            2. Calculate Path
                2-1: the path from current position to source station which is in the task.
                2-2: the path from source staion to target station.
        '''
        # deal task
        task = TaskQueue.FetchSingleTask()
        if task != None:
            agv = AgvBotQueue.FetchSingleAGV()
            if agv != None:
                cls.Plan(task,agv)
                # Update path plan to MQTT
                task.State = Task.States["Planed"]




if __name__ == '__main__':
    myScheduler = AgvScheduler()
    # myCommuUpper = CommuUpper()
    AgvBotQueue.init(3)

    def onMqttReceived():
        # AGV state is updated
        mqtt_topic = "agv/123/state"
        mqtt_message = "Idle"
        AgvBotQueue.UpdateAgvState()


    while True:
        # onMqttReceived()
        # myCommuUpper.SpinOnce()
        task_id = 1
        source_station = 2
        target_station = 3
        TaskQueue.AppendTask(task_id, source_station, target_station)

        AgvScheduler.SpinOnce()
        print(TaskQueue.show())
        time.sleep(2)


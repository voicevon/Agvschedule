

import time

from bolt_nut import AgvBotAgent, Task, TaskQueue, AgvBotAgent, AgvBotQueue,CommuUpper


class AgvScheduler():
    '''
    
    '''
    track_nodes_count = 8
    def __init__(self) -> None:
        pass

    @classmethod            
    def GetTrackPath(cls, start_point, end_point) -> list:
        path = []
        point = start_point
        if start_point > end_point:
            end_point += cls.track_nodes_count
        while point < end_point:
            point += 1
            path.append(point % cls.track_nodes_count)
        return path

    @classmethod
    def Plan(cls, task: Task, bot:AgvBotAgent):
        task.AgvBot = bot
        # calculate path to source point
        path_to_source = cls.GetTrackPath(bot.current_point, task.SourceStation_id)
        # calculate path to target point
        path_to_target = cls.GetTrackPath(bot.path_to_source,task.TargetStation_id)
        bot.StartTask(path_to_source, path_to_target)

    @classmethod
    def SpinOnce(cls) -> None:
        '''
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
    myCommuUpper = CommuUpper()
    AgvBotQueue.init(3)

    def onMqttReceived():
        # AGV state is updated
        mqtt_topic = "agv/123/state"
        mqtt_message = "Idle"
        AgvBotQueue.UpdateAgvState()


    while True:
        # onMqttReceived()
        myCommuUpper.SpinOnce()
        AgvScheduler.SpinOnce()
        time.sleep(2)
        print(TaskQueue.show())

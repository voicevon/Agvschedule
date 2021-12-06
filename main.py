

import time

from bolt_nut import Task, TaskQueue, AgvBot, AgvBotQueue,CommuUpper


class AgvScheduler():
    '''
    
    '''
    def __init__(self) -> None:
        self.track_nodes_count = 8
            

    def GetTrackPath(self, start_point, end_point) -> list:
        path = []
        point = start_point
        if start_point > end_point:
            end_point += self.track_nodes_count
        while point < end_point:
            point += 1
            path.append(point % self.track_nodes_count)
        return path

    def Plan(self, task: Task, bot:AgvBot):
        task.AgvBot = bot
        # calculate path to source point
        bot.path_to_source = self.GetTrackPath(bot.current_point, task.SourceStation_id)
        # calculate path to target point
        bot.path_to_target = self.GetTrackPath(bot.path_to_source,task.TargetStation_id)

    def SpinOnce(self) -> None:
        '''
        '''
        # deal task
        task = TaskQueue.FetchSingleTask()
        if task != None:
            agv = AgvBotQueue.FetchSingleAGV()
            if agv != None:
                self.Plan(task,agv)
                # Update path plan to MQTT
                task.State = Task.States["Planed"]



if __name__ == '__MAIN__':
    myScheduler = AgvScheduler()
    myCommuUpper = CommuUpper()

    while True:
        myCommuUpper.SpinOnce()
        myScheduler.SpinOnce()
        time.sleep(0.1)


class WorkStation:
    def __init__(self) -> None:
        pass


# AGVBOT_STATE = ["Idle", "MovingToSource", "Loading","MovingToTarget","OffLoading"]  #???

class AgvBotAgent:
    AGVBOT_STATE = {"Idle":1,"":2}

    def __init__(self, bot_id) -> None:
        self.id = bot_id
        self.State = self.AGVBOT_STATE["Idle"]
        self.current_point = 0
        self.current_task: Task
        self.path_to_source = []
        self.path_to_target = []

    def StartTask(self, path_to_source, path_to_target):
        self.path_to_source =  path_to_source
        self.path_to_target = path_to_target
        # self.State = AGVBOT_STATE["MovingToSource"]  #???
        
        # publish a message via MQTT
        # topic and message are:   
        #   agv/123/path_to_source:     a/123/ps
        #        (1,true),(2,true),(3,false),(4,true),(5,true)c
        #   agv/123/path_to_target:     a/123/pt
        #        (8,true),(11,true),(15,false),(16,true),(17,true)
        #   true/false  == follow_right_track
   




class AgvBotQueue():
    agvbots = []

    def __init__(self, total_agv_count = 3) -> None:
        pass

    @classmethod
    def init(cls, total_agv_count):
        for i in range(total_agv_count):
            new_bot = AgvBotAgent(i)
            cls.agvbots.append(new_bot)

    @classmethod
    def FetchSingleAGV(cls) -> AgvBotAgent:
        '''
        Core function of the system.
        Mainly will do:
            1. Select an AGV, 
            2. Will Calculate Paths in other functions
                2-1: the path from current position to source station which is in the task.
                2-2: the path from source staion to target station.
        This can be very complex!
        '''
        for bot in cls.agvbots:
            if bot.State == 'Idle':
                return bot
        # All agv bots are busy
        return None

    @classmethod
    def GetBotFromId(cls, bot_id:int) -> AgvBotAgent:
        return None

    @classmethod
    def onReceivedMqtt(cls, topic, message):
        # Sync to local bot state, etc.  For reading it faster.
        bot_id = 1
        bot = cls.GetBotFromId(bot_id)
        bot.State = 1

    @classmethod
    def UpdateAgvState(cls, id: int, current_point: int, state: str) -> None:
        '''
        This function is a callback of MQTT subscription.
        '''
        bot = cls.GetBotFromId(id)
        bot.current_point = current_point
        bot.State = state



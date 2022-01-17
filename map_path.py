
class Map：
    '''
    This is a 2D map.   Stations(Work stations and Battery charge station) are sit on.
    Will help to find a path from Station-A to Station-B
        1. Points Can be identified by RFid reader. or QR-code reader.
        2. Track might be spilited in from of a Point.
    For Version 1.0, We consider the simplest path
        1. The track is a ring, only one branch.
        2A. Follow left branch, will move to next work station.
        2B. Follow right branch, will move to Battery Charge station.

.                       <------ Battery Charge Station  <----
.                      /                                     \
.                     /<------ WS-20  <--------  WS-19 <------O---- WS-18 <---
.                    /                                                         \
.                  WS-1                                                       WS-6
.                    \                                                         /
.                      -------> WS-2  ------> WS-3   ----> WS-4  ----> WS-5 --/  
    '''
    
    Stations = []

    @staticmethod
    def Init():
        for i in range(20):
            Map.Stations.append(i)

    

        
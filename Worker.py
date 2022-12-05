import time

class Worker:

    def __init__(self):
        self.isOccupied = False
        self.visitedTimes = 0
        self.totalWorkTime = 0.0
        # pass

    # def recognize(self) -> str:
    def recognize(self, str_data) -> str:
        # start timing
        startTime = time.time()

        # update worker's status to "occupied"
        self.isOccupied = True
        self.visitedTimes += 1

        '''
        recognizing process
        '''

        # end timing
        endTime = time.time()
        # total processing time
        timeCost = endTime - startTime

        self.totalWorkTime += timeCost

        timeCost = str(timeCost)

        '''
        could return a list of string, including recognizing result and total cost of time
        
        e.g
        resultList = [result, timeCost]
        '''

    # for analysis
    def getStatistics(self):
        return [self.visitedTimes, self.totalWorkTime]


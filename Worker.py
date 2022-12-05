import time

class Worker:

    def __init__(self):
        self.isOccupied = False
        self.visitedTimes = 0
        # pass

    def recognize(self) -> str:

        # update worker's status to "occupied"
        self.isOccupied = True
        self.visitedTimes += 1



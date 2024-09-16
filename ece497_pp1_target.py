import numpy as np
import math

class Target():

    def __init__(self):
        self.x = 2
        self.y = 2
    
    def calculateAgentAngleAndDistanceFromTarget(self, agentSensorXPos, agentSensorYPos):
        xPosDiff = agentSensorXPos - self.x
        yPosDiff = agentSensorYPos - self.y
        distanceFromAgent = math.sqrt(xPosDiff**2 + yPosDiff**2)
        angleAgentFromTarget = math.atan(float(yPosDiff)/float(xPosDiff))
        return distanceFromAgent, angleAgentFromTarget
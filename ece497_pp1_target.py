import numpy as np
import math

class Target():
    """Defines the object to which the agent is attracted in Part Four."""

    def __init__(self):
        self.x = 2
        self.y = 2
    
    def calculateAgentAngleAndDistanceFromTarget(self, agentSensorXPos, agentSensorYPos):
        """Calculates the distance and angle between an agent's sensor and the target."""
        xPosDiff = agentSensorXPos - self.x
        yPosDiff = agentSensorYPos - self.y
        distanceFromAgent = math.sqrt(xPosDiff**2 + yPosDiff**2)
        angleAgentFromTarget = math.atan(float(yPosDiff)/float(xPosDiff))
        return distanceFromAgent, angleAgentFromTarget
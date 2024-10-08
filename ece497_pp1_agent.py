import numpy as np
import math

class Agent():
    """The vehicle used as the random walker."""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.sensorOffset = 0.50
        self.sensorLeftX = self.x - self.sensorOffset
        self.sensorLeftY = self.y
        self.sensorRightX = self.x + self.sensorOffset
        self.sensorRightY = self.y
        self.orientation = 0
        self.velocity = 1
        self.p = 1 # probability
        self.distance = 0
    
    def basicStep(self):
        # Used for Parts One, Two, and Three
        self.orientation += np.random.random() * 2 * np.pi # orientation is randomized
        self.x += self.velocity * np.cos(self.orientation)
        self.y += self.velocity * np.sin(self.orientation)
        self.sensorLeftX = self.x - self.sensorOffset
        self.sensorLeftY = self.y
        self.sensorRightX = self.x + self.sensorOffset
        self.sensorRightY = self.y

    def step(self):
        # Used for Part Four
        # Orientation is set in simulation
        self.x += self.velocity * np.cos(self.orientation)
        self.y += self.velocity * np.sin(self.orientation)
        self.sensorLeftX = self.x - self.sensorOffset
        self.sensorLeftY = self.y
        self.sensorRightX = self.x + self.sensorOffset
        self.sensorRightY = self.y

    def calculateDistanceAwayFromOrigin(self):
        self.distance = math.sqrt(self.x**2 + self.y**2) # Pythagorean Theorem
        return self.distance

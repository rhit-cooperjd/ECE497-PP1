import ece497_pp1_agent as agent
import ece497_pp1_target as target
import matplotlib.pyplot as plt
import numpy as np
import math

def runPartTwo():
    n = int(input("Please enter the number of steps you would like the agent to take: "))
    distanceList = makeIndSimGraph(n)
    makeIndDistanceFromOriginGraph(n, distanceList)

def runPartThree():
    n = int(input("Please enter the number of steps you would like the agent to take: "))
    popsize = int(input("Please enter the desired population size: "))
    distanceList = makeGroupSimGraph(popsize, n)
    makeGroupDistancesFromOriginGraph(popsize, n, distanceList)

def runPartFour():
    n = int(input("Please enter the number of steps you would like the agent to take: "))
    popsize = int(input("Please enter the desired population size: "))
    successes, failures = runGroupAttractionSim(popsize, n)
    showResults(successes, failures)
    
def runIndSim(n):
    """Models the random travel of a single agent."""
    walker = agent.Agent()
    xlist = np.zeros(n+1)
    ylist = np.zeros(n+1)
    distanceList = np.zeros(n+1)
    for i in range(n):
        walker.basicStep()
        xlist[i + 1] = walker.x
        ylist[i + 1] = walker.y
        distanceList[i+1] = walker.calculateDistanceAwayFromOrigin()
    return xlist, ylist, distanceList

def makeIndSimGraph(n):
    """Visually displays the results of Part Two."""
    x, y, distanceList = runIndSim(n)
    plt.plot(x, y)
    plt.plot(0,0,'ro')
    plt.plot(x[-1], y[-1], 'ko')
    plt.title("Individual Agent Simulation with {} Steps".format(n))
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
    return distanceList

def makeIndDistanceFromOriginGraph(n, distanceList):
    """Visually displays the results of Part Two."""
    nlist = np.zeros(n+1)
    for i in range(n):
        nlist[i] = i
    plt.stem(nlist, distanceList) # Stem plot is appropriate since steps are discrete.
    plt.title("Individual Agent's Travel From Origin")
    plt.xlabel("Step")
    plt.ylabel("Distance From Origin")
    plt.show()

def runGroup(popsize, n):
    """Simulation for Part 3."""
    xlist = np.zeros((popsize,n+1))
    ylist = np.zeros((popsize,n+1))
    distancesList = np.zeros((popsize,n+1))
    for i in range(popsize):
        xlist[i], ylist[i], distancesList[i] = runIndSim(n)
    return xlist, ylist, distancesList

def makeGroupSimGraph(popsize, n):
    """Displays results from Part Three."""
    x, y, distancesList = runGroup(popsize, n)
    plt.plot(0, 0, 'ro')
    for i in range(popsize):
        plt.plot(x[i], y[i])
        plt.plot(x[i][-1], y[i][-1], 'ko')
    plt.title("Group Agent Simulation of Population {} and {} Steps".format(popsize, n))
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
    return distancesList

def makeGroupDistancesFromOriginGraph(popsize, n, distancesList):
    """Displays results from Part Three."""
    nlist = np.zeros(n+1)
    average = np.mean(distancesList, axis=0)
    for i in range(n):
        nlist[i] = i
    for j in range(popsize):
        plt.scatter(nlist, distancesList[j])
    plt.plot(nlist, average, 'ko')
    plt.title("Group Agent's Travel From Origin")
    plt.xlabel("Step")
    plt.ylabel("Distance From Origin")
    plt.show()

def probabilityScaler(distance):
    """Used in Part Four to provide error in setting the orientation based on distance from target."""
    p = 0.50
    if distance < 5:
        p = np.random.uniform(0.95, 1)
    elif distance < 10: 
        p = np.random.uniform(0.85, 1)
    elif distance < 30:
        p = np.random.uniform(0.60, 1)
    else:
        p = 0.50
    return p

def printStats(walker, sensorDistance, sensorAngle, index):
    print("======== Step #{} ========".format(index))
    print("agent sensor distance from target: " + str(sensorDistance))
    print("agent sensor angle from target: " + str(sensorAngle))
    print("walker probability scaler: " + str(walker.p))
    print("walker new orientation: " + str(walker.orientation))

def runIndAttractionSim(n):
    """Part Four simulation for a single agent."""
    walker = agent.Agent()
    destination = target.Target()
    xlist = np.zeros(n+1)
    ylist = np.zeros(n+1)
    successCount = 0
    for i in range(n):
        leftSensorDistanceFromTarget, leftSensorAngleFromTarget = destination.calculateAgentAngleAndDistanceFromTarget(walker.sensorLeftX, walker.sensorLeftY)
        rightSensorDistanceFromTarget, rightSensorAngleFromTarget = destination.calculateAgentAngleAndDistanceFromTarget(walker.sensorRightX, walker.sensorRightY)
        if leftSensorDistanceFromTarget < rightSensorDistanceFromTarget:
            walker.p = probabilityScaler(leftSensorDistanceFromTarget)
            walker.orientation = (walker.p * leftSensorAngleFromTarget)
            printStats(walker, leftSensorDistanceFromTarget, leftSensorAngleFromTarget, i+1)
        else:
            walker.p = probabilityScaler(rightSensorDistanceFromTarget)
            walker.orientation = (walker.p * rightSensorAngleFromTarget)
            printStats(walker, leftSensorDistanceFromTarget, leftSensorAngleFromTarget, i+1)
        walker.step()
        if abs(walker.x - destination.x) <=  walker.sensorOffset and abs(walker.y - destination.y) <= walker.sensorOffset:
            successCount += 1
        xlist[i + 1] = walker.x
        ylist[i + 1] = walker.y
        walker.orientation = 0
    plt.plot(xlist, ylist)
    plt.plot(0,0,'ro')
    plt.plot(xlist[-1], ylist[-1], 'ko')
    plt.plot(destination.x, destination.y, 'bo')
    plt.title("Individual Agent Simulation with {} Steps".format(n))
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

def runGroupAttractionSim(popsize, n):
    """Part Four simulation for a population of agents."""
    walkerList = [] # Contains the agents
    totalRuns = popsize
    for j in range(popsize):
        walker = agent.Agent()
        walkerList.append(walker)
    destination = target.Target()
    xlist = np.zeros((popsize,n+1))
    ylist = np.zeros((popsize,n+1))
    successCount = 0
    lock = False
    plt.plot(0,0,'ro')
    for k in range(popsize):
        lock = False
        walker = walkerList[k]
        for i in range(n):
            leftSensorDistanceFromTarget, leftSensorAngleFromTarget = destination.calculateAgentAngleAndDistanceFromTarget(walker.sensorLeftX, walker.sensorLeftY)
            rightSensorDistanceFromTarget, rightSensorAngleFromTarget = destination.calculateAgentAngleAndDistanceFromTarget(walker.sensorRightX, walker.sensorRightY)
            if leftSensorDistanceFromTarget < rightSensorDistanceFromTarget:
                walker.p = probabilityScaler(leftSensorDistanceFromTarget)
                walker.orientation = (walker.p * leftSensorAngleFromTarget)
                printStats(walker, leftSensorDistanceFromTarget, leftSensorAngleFromTarget, i+1)
            else:
                walker.p = probabilityScaler(rightSensorDistanceFromTarget)
                walker.orientation = (walker.p * rightSensorAngleFromTarget)
                printStats(walker, leftSensorDistanceFromTarget, leftSensorAngleFromTarget, i+1)
            walker.step()
            if abs(walker.x - destination.x) <=  0.40 and abs(walker.y - destination.y) <= 0.40 and lock == False:
                successCount += 1
                lock = True
            xlist[k][i + 1] = walker.x
            ylist[k][i + 1] = walker.y
            walker.orientation = 0
            plt.plot(xlist[k], ylist[k])
            plt.plot(xlist[k][-1], ylist[k][-1], 'ko')
    plt.plot(destination.x, destination.y, 'bo')
    plt.title("Group Agent Simulation with Population {} and {} Steps".format(popsize, n))
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
    failureCount = totalRuns - successCount
    return successCount, failureCount

def showResults(successes, failures):
    fig, ax = plt.subplots()
    bar_labels = ['successes', 'failures']
    bar_colors = ['tab:green', 'tab:red']
    result = ['Success', 'Failure']
    count = [successes, failures]
    ax.bar(result, count, label=bar_labels, color=bar_colors)
    plt.title('Group Attraction Simulation Results')
    plt.show()


runPartTwo()
runPartThree()
runPartFour()



# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#
# THIS  CODE  WAS MY OWN WORK , IT WAS  WRITTEN  WITHOUT  CONSULTING  ANY# SOURCES  OUTSIDE  OF THOSE  APPROVED  BY THE  INSTRUCTOR. Abdullah Hamid

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood() #food available from current state
        newFood = successorGameState.getFood() #food available from successor state (excludes food@successor) 
        currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        finalScore = 0.0
        ghostDistance = []
        for ghost in newGhostStates:
            ghostPosition = ghost.getPosition()
            distance = manhattanDistance(ghostPosition, newPos)
            ghostDistance.append(distance)
        for i in ghostDistance:
            factor = 1
            if (i <= 1):
                if (ghost.scaredTimer == 0):
                    finalScore -= 200
                else:
                    finalScore += 1500
                    factor = -1
        capsuleState = currentGameState.getCapsules()
        capsuleDistance = []
        for capsule in capsuleState:
            b = manhattanDistance(capsule, newPos)
            capsuleDistance.append(b)
        for i in capsuleDistance:
            if (b == 0):
                finalScore += 100
            else:
                finalScore += (10.0 / b)
        theFood = currentGameState.getFood()
        foodList = theFood.asList()
        foodPos = []
        for k in foodList:
            a = manhattanDistance(k, newPos)
            foodPos.append(a)
        for i in foodPos:
            if (i == 0):
                finalScore = finalScore + 100
            else:
                finalScore = finalScore + (1.0 / (i ** 2))
        return finalScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        actionScore = []
        def minimax(state, counter):
            if counter >= numAgents * self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if not counter % numAgents:
                result = -999999999999
                for action in state.getLegalActions(0):
                    newState = state.generateSuccessor(0, action)
                    result = max(result, minimax(newState, counter + 1))
                    if not counter:
                        actionScore.append(result)
                return result
            else:
                result = 999999999999
                for action in state.getLegalActions(counter % numAgents):
                    newState = state.generateSuccessor(counter % numAgents, action)
                    result = min(result, minimax(newState, counter + 1))
                return result
        result = minimax(gameState, 0)
        return gameState.getLegalActions()[actionScore.index(max(actionScore))]
        util.raiseNotDefined()
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        actionScore = []
        def alphaBeta(state, iterCount, alpha, beta):
            if iterCount >= numAgents * self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            if not iterCount % numAgents:
                result = -999999999999
                for action in state.getLegalActions(0):
                    newState = state.generateSuccessor(0,action)
                    result = max(result, alphaBeta(newState, iterCount + 1, alpha, beta))
                    if not iterCount:
                        actionScore.append(result)
                    if result > beta:
                        return result
                    alpha = max(result, alpha)
                return result
            else:
                result = 999999999999
                for action in state.getLegalActions(iterCount % numAgents):
                    newState = state.generateSuccessor(iterCount % numAgents, action)
                    result = min(result, alphaBeta(newState, iterCount + 1, alpha, beta))
                    if result < alpha:
                        return result
                    beta = min(result, beta)
                return result
        result = alphaBeta(gameState, 0, -999999999999, 999999999999)
        return gameState.getLegalActions()[actionScore.index(max(actionScore))]
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        numAgents = gameState.getNumAgents()
        actionScore = []

        def expectimax(state, iterCount):
            if iterCount >= numAgents * self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if not iterCount % numAgents:
                result = -999999999999
                for action in state.getLegalActions(0):
                    newState = state.generateSuccessor(0,action)
                    result = max(result, expectimax(newState, iterCount + 1))
                    if not iterCount:
                        actionScore.append(result)
                return result
            else:
                scores = list()
                for action in state.getLegalActions(iterCount % numAgents):
                    newState = state.generateSuccessor(iterCount % numAgents, action)
                    scores.append(expectimax(newState, iterCount + 1))
                return sum(scores) * 1.0 / len(scores)

        result = expectimax(gameState, 0)
        return gameState.getLegalActions()[actionScore.index(max(actionScore))]
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return float("inf")
    elif currentGameState.isLose():
        return - float("inf")
    score = scoreEvaluationFunction(currentGameState)
    current_state = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    foodList = food.asList()
    foodPos = []
    for k in foodList:
        a = manhattanDistance(k, current_state)
        foodPos.append(a)
    for i in foodPos:
        if (i == 0):
            score = score + 100
        else:
            score = score + (1.0 / (i ** 2))
    ghostList = currentGameState.getGhostStates()
    ghostDistance = []
    scaredGhost = []
    distance = []
    for ghost in ghostList:
        ghostPosition = ghost.getPosition()
        pos = manhattanDistance(current_state, ghostPosition)
        distance.append(pos)
        if ghost.scaredTimer == 0:
            ghostDistance += distance
        elif ghost.scaredTimer > 0:
            scaredGhost += distance
    minGhostDistance = -1
    minScaredGhostdistance = -1
    if len(ghostDistance) > 0:
        minGhostDistance = min(ghostDistance)
    elif len(scaredGhost) > 0:
        minScaredGhostdistance = min(scaredGhost)
    score -= (2 / minGhostDistance)
    score -= (2 * minScaredGhostdistance)
    capsules = currentGameState.getCapsules()
    capsuleLen = len(capsules)
    score = score - (15 * capsuleLen)
    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"

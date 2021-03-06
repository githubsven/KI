# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    # Grab starting state of the problem. If this state already satisfies the problem, return that no action needs to be taken
    currentState = problem.getStartState()
    if problem.isGoalState(currentState) == True:
        return []
    # DFS uses a stack, bfs is the same as this method, but instead of a stack it uses a queue
    stack = util.Stack()
    stack.push((currentState, [], []))

    visited = []
    #keep searching until the stack is empty, or if the goal is found
    while stack.isEmpty() == False:
        # Get first option
        currentState, currentDirections, currentCost = stack.pop()
        if problem.isGoalState(currentState):
            return currentDirections
        # We keep a list visited, so we can't go back the way we came from
        if currentState not in visited:
            visited.append(currentState)
            # Push all new successors to the stack
            for state, action, cost in problem.getSuccessors(currentState):
                stack.push((state, currentDirections + [action], currentCost + [cost]))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    currentState = problem.getStartState()
    if problem.isGoalState(currentState) == True:
        return []
    # Roughly the same as DFS, but using a Queue item instead of a stack.
    # This causes the search to traverse the tree down each branch at the same pace instead of down one branch fully before going down another
    Queue = util.Queue()
    Queue.push((currentState, [], []))

    visited = []

    while Queue.isEmpty() == False:
        currentState, currentDirections, currentCost = Queue.pop()
        if problem.isGoalState(currentState):
            return currentDirections
            
        if currentState not in visited:
            visited.append(currentState)
            for state, action, cost in problem.getSuccessors(currentState):
                Queue.push((state, currentDirections + [action], currentCost + [cost]))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    currentState = problem.getStartState()
    if problem.isGoalState(currentState) == True:
        return []

    # Similar to DFS and BFS, but using a priorityQueue. By linking each element in the queue to a cost, and "popping" the lowest cost first
    # The "cheapest" path is always explored first. This results in behaviour roughly like the BFS, but taking a given "cost" into account
    prioQ = util.PriorityQueue()
    prioQ.push((currentState, [], 0), 0)

    visited = []
    resultCost = 9223372036854775807
    resultDirections = []

    while not prioQ.isEmpty():
        currentState, currentDirections, currentCost = prioQ.pop()

        if problem.isGoalState(currentState) & (currentCost < resultCost):
            resultDirections = currentDirections
            resultCost = currentCost

        if (currentState not in visited) & (not problem.isGoalState(currentState)) & (currentCost < resultCost):
            visited.append(currentState)

            for state, action, cost in problem.getSuccessors(currentState):
                prioQ.push((state, currentDirections + [action], currentCost + cost), currentCost + cost)

    return resultDirections

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    openSet = util.PriorityQueue()
    openSet.push((problem.getStartState(), [],0), heuristic(problem.getStartState(), problem))

    # Very similar to UCS. By using a heuristic, the cost of the path so far and the estimated cost from a node to the goal
    # are combined to get a more accurate cost per explored node.

    visited = []
    expanded = []
    while not openSet.isEmpty():
        currentState, actions,c = openSet.pop()
        if problem.isGoalState(currentState):
            return actions

        if currentState not in expanded:
            expanded.append(currentState)

            for successor, action, cost in problem.getSuccessors(currentState):
               newCost = c + cost
               if successor not in visited:
                    priority = newCost + heuristic(successor, problem)
                    openSet.push((successor, actions + [action],newCost), priority)
                    visited.append(currentState)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

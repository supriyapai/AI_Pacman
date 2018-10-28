# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
from heuristics import *
import random


class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0, len(actions) - 1)]


class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)


class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP


        winState=[]
        legal = state.getLegalPacmanActions()
        nonetype_flag = 0
        fringes = [(state.generatePacmanSuccessor(actions), actions) for actions in legal]

        while (fringes):
            if (nonetype_flag == 1):
                break
            path, actions = fringes.pop(0)

            if (path.isWin()):
                winState.append((path, actions))
                print "win state"
                return actions

            legal = path.getLegalPacmanActions()

            for next_actions in legal:
                next_fringe = path.generatePacmanSuccessor(next_actions)
                if (next_fringe == None):
                    nonetype_flag = 1
                    break
                fringes.append((next_fringe, actions))


        if len(winState) != 0:
            # if winState has nodes, append it to the scored list
            scored = [(admissibleHeuristic(state), actions) for state, actions in winState]

        # If not reaching a terminal state, return the actions leading to the node with
        # the best score and no children based on the heuristic function (admissibleHeuristic)
        if (fringes):
            scored = [(admissibleHeuristic(state), actions) for state, actions in fringes]
            bestScore = min(scored)[0]
            bestactions = [pair[1] for pair in scored if pair[0] == bestScore]

        # return random actions from the list of the best actionss
        return random.choice(bestactions)
        return Directions.STOP


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts

    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP

        noneFlag = 0
        winState = []
        legal = state.getLegalPacmanActions()
        fringes = [(state.generatePacmanSuccessor(actions), actions) for actions in legal]

        while (fringes):
            if (noneFlag == 1):
                break
            path, actions = fringes.pop(-1)

            if (path.isWin()):
                winState.append((path, actions))
                print "win state"
            return actions

            legal = path.getLegalPacmanActions()

            for next_actions in legal:
                next_fringe = path.generatePacmanSuccessor(next_actions)
                if (next_fringe == None):
                    noneFlag = 1
                    break
                fringes.append((next_fringe, actions))

        if len(winState) != 0:
            # if winState has nodes, append it to the scored list
            scored = [(admissibleHeuristic(state), actions) for state, actions in winState]


        # If not reaching a terminal state, return the actions leading to the node with
        # the best score and no children based on the heuristic function (admissibleHeuristic)
        if (fringes):
            scored = [(admissibleHeuristic(state), actions) for state, actions in fringes]
            bestScore = min(scored)[0]
            bestactions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random actions from the list of the best actionss
        return random.choice(bestactions)
        return Directions.STOP


class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        noneFlag = 0
        fringes = []
        winState = []
        end = []
        scored = []

        legal = state.getLegalPacmanActions()
        depth = 1

        for actions in legal:
            intial_fringe = state.generatePacmanSuccessor(actions)
            cost = depth - (admissibleHeuristic(intial_fringe) - admissibleHeuristic(state))
            fringes.append((cost, intial_fringe, actions, depth))

        while (fringes):
            if (noneFlag == 1):
                break

            sort_cost = fringes.index(min(fringes))
            cost, path, actions, depth = fringes.pop(sort_cost)

            if (path.isWin()):
                winState.append((path, actions))
                return actions

            legal = path.getLegalPacmanActions()

            for next_action in legal:
                next_fringe = path.generatePacmanSuccessor(next_action)
                if (next_fringe == None):
                    end.append((path, actions))
                    noneFlag = 1
                    break

                cost = (depth + 1) - (admissibleHeuristic(path) - admissibleHeuristic(state))
                fringes.append((cost, next_fringe, actions, depth + 1))

        # If not reaching a terminal state, return the action leading to the node with
        # the best score and no children based on the heuristic function (admissibleHeuristic)

        if len(winState) != 0:
            # if winState has nodes, append it to the scored list
            scored = [(admissibleHeuristic(state), actions) for state, actions in winState]

        if (fringes):
            scored = [(admissibleHeuristic(state), actions) for cost, state, actions, depth in fringes]
            bestScore = min(scored)[0]
            bestactions = [pair[1] for pair in scored if pair[0] == bestScore]

            return random.choice(bestactions)
        return Directions.STOP

import random, sys
from mastermind import board
import pickle


colors = list(range(6))
colorConversion = {0: 'R', 1: 'G', 2: 'S', 3: 'Y', 4: 'B', 5: 'W'}

class solver(object):
    def __init__(self):
        self.moves = []
        self.history = []

        for first in range(6):
            for second in range(6):
                for third in range(6):
                    for fourth in range(6):
                        self.moves.append([first, second, third, fourth])
        
        self.allMoves = self.moves.copy()
        
    def makeGuess(self):
        pass
    
    def adjustMoves(self, guess, response):
        self.history.append((tuple(guess), tuple(response)))
        self.moves = self.prune(guess, response)
    
    def prune(self, guess, response) -> list[list]:
        newMoves = self.moves.copy()
        for move in self.moves.copy():
            moveCopy = move.copy()
            guessCopy = guess.copy()

            blackPins = 0
            whitePins = 0

            for m, g in zip(move, guess):
                if m == g:
                    moveCopy.remove(m)
                    guessCopy.remove(g)
                    blackPins += 1

            for m in moveCopy:
                if m in guessCopy:
                    guessCopy.remove(m)
                    whitePins += 1
                
            if blackPins == response[0] and whitePins == response[1]:
                continue
            else:
                newMoves.remove(move)
        
        return newMoves

class random_solver(solver):
    def makeGuess(self):
        return random.choice(self.moves)

class most_occurences(solver):
    def makeGuess(self):
        first = {}
        second = {}
        third = {}
        fourth = {}
        
        for move in self.moves:
            first[move[0]] = first.get(move[0], 0)
            second[move[1]] = second.get(move[1], 0)
            third[move[2]] = third.get(move[2], 0)
            fourth[move[3]] = fourth.get(move[3], 0)
        
        one = max(first, key=first.get)
        two = max(second, key=second.get)
        three = max(third, key=third.get)
        four = max(fourth, key=fourth.get)
        potGuess = [one, two, three, four]
        
        if potGuess in self.moves:
            return potGuess

class mini_max_shortened(solver):
    def __init__(self):
        super().__init__()
        self.pinCombos = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (3, 0)]
    
    def makeGuess(self):
        if len(self.history) == 0:
            return [0, 0, 1, 1]
        
        if len(self.moves) == 1:
            return self.moves[0]
        
        minimax = sys.maxsize

        minimaxedMove = None

        for move in self.moves:
            # Don't guess a previously made move
            if move in [a[1] for a in self.history]:
                continue

            localMax = 0

            for pin in self.pinCombos:
                localMax = max(localMax, len(self.prune(move, pin)))

            if localMax > 0 and localMax < minimax:
                minimaxedMove = move
                minimax = localMax

        if minimaxedMove is not None:
            return minimaxedMove
        else:
            random.choice(self.moves)

class mini_max_extended(solver):
    miniMaxLookup = {}
    
    def __init__(self):
        super().__init__()
        self.pinCombos = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (3, 0)]
    
    def makeGuess(self):
        if len(self.history) == 0:
            return [0, 0, 1, 1]
        
        if len(self.moves) == 1:
            return self.moves[0]
        
        if tuple(self.history) in mini_max_extended.miniMaxLookup:
            return mini_max_extended.miniMaxLookup[tuple(self.history)]
        
        minimax = sys.maxsize

        minimaxedMove = None

        for move in self.allMoves:
            # Don't guess a previously made move
            if move in [a[1] for a in self.history]:
                continue

            localMax = 0

            for pin in self.pinCombos:
                localMax = max(localMax, len(self.prune(move, pin)))

            if localMax > 0 and localMax < minimax:
                minimaxedMove = move
                minimax = localMax

        if minimaxedMove is not None:
            mini_max_extended.miniMaxLookup[tuple(self.history)] = minimaxedMove
            return minimaxedMove
        else:
            random.choice(self.moves)
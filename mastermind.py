import random


class board(object):
    def __init__(self):
        self.key : list[int] = random.choices(range(6), k=4)
        self.history = []
    
    def makeGuess(self, guessList: list[int]) -> tuple[int]:
        keyCopy = self.key.copy()
        guessCopy = guessList.copy()

        blackPins = 0
        whitePins = 0

        for key, guess in zip(self.key, guessList):
            if key == guess:
                keyCopy.remove(key)
                guessCopy.remove(guess)
                blackPins += 1

        for guess in guessCopy:
            if guess in keyCopy:
                keyCopy.remove(guess)
                whitePins += 1

        self.history.append((guessList, (blackPins, whitePins)))

        return (blackPins, whitePins)
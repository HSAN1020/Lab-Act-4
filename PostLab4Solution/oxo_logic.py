"""
This is the main logic for a Tic-tac-toe game (OOP version).
It generates random moves and checks the results of a move for a winning line.
Exposed methods are:
- newGame()
- saveGame()
- restoreGame()
- userMove()
- computerMove()
"""

import os, random
import oxo_data

class Game:
    def __init__(self, game=None):
        if game and len(game) == 9:
            self.game = game
        else:
            self.game = [" "] * 9

    def newGame(self):
        """Reset to new empty game"""
        self.game = [" "] * 9
        return self.game

    def saveGame(self):
        """Save game to disk"""
        oxo_data.saveGame(self.game)

    def restoreGame(self):
        """Restore previously saved game.
        If not successful, return new game.
        """
        try:
            game = oxo_data.restoreGame()
            if len(game) == 9:
                self.game = game
            else:
                self.newGame()
        except IOError:
            self.newGame()
        return self.game

    def _generateMove(self):
        """Generate a random cell from those available.
        If all cells are used, return -1
        """
        options = [i for i in range(len(self.game)) if self.game[i] == " "]
        return random.choice(options) if options else -1

    def _isWinningMove(self):
        """Check if the current state has a winning line"""
        wins = ((0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6))

        for a, b, c in wins:
            chars = self.game[a] + self.game[b] + self.game[c]
            if chars == "XXX" or chars == "OOO":
                return True
        return False

    def userMove(self, cell):
        """Make a move for the user ('X')"""
        if self.game[cell] != " ":
            raise ValueError("Invalid cell")
        else:
            self.game[cell] = "X"

        if self._isWinningMove():
            return "X"
        return ""

    def computerMove(self):
        """Make a move for the computer ('O')"""
        cell = self._generateMove()
        if cell == -1:
            return "D"
        self.game[cell] = "O"
        if self._isWinningMove():
            return "O"
        return ""

    def playTest(self):
        """Simple test loop to demonstrate gameplay"""
        result = ""
        self.newGame()
        while not result:
            print(self.game)
            try:
                result = self.userMove(self._generateMove())
            except ValueError:
                print("Oops, that shouldn't happen")

            if not result:
                result = self.computerMove()

            if not result:
                continue
            elif result == "D":
                print("It's a draw")
            else:
                print("Winner is:", result)
            print(self.game)


if __name__ == "__main__":
    game = Game()
    game.playTest()

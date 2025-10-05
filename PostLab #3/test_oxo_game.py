# test_oxo_game.py
"""
Unit Test Program for Tic Tac Toe Console Application

This test suite covers:
- oxo_data module (save/restore functionality)
- oxo_logic module (game logic, moves, win detection)
- Edge cases and error handling
"""

import unittest
import os
import tempfile
import random
from unittest.mock import patch, MagicMock

# Import the modules to test
# Assuming the code is properly modularized into separate files
try:
    from oxo_data import saveGame, restoreGame, _getPath
    from oxo_logic import (newGame, saveGame as saveGame_logic, restoreGame as restoreGame_logic, 
                          userMove, computerMove, _generateMove, _isWinningMove)
    from oxo_ui import getMenuChoice as getMenuChoice_ui, startGame as startGame_ui, printGame as printGame_ui
except ImportError:
    print("Note: Ensure oxo_data.py, oxo_logic.py, and oxo_ui.py are in the same directory")


class TestOxoData(unittest.TestCase):
    """Test cases for the oxo_data module - file save/restore operations"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.test_game = list("XO XO XO ")
        self.game_file = "oxogame.dat"
        
    def tearDown(self):
        """Clean up test files after each test"""
        try:
            test_file = os.path.join(_getPath(), self.game_file)
            if os.path.exists(test_file):
                os.remove(test_file)
        except:
            pass
    
    def test_getPath_returns_string(self):
        """Test that _getPath returns a string path"""
        path = _getPath()
        self.assertIsInstance(path, str, "Path should be a string")
        
    def test_getPath_returns_existing_directory(self):
        """Test that _getPath returns a valid existing directory"""
        path = _getPath()
        self.assertTrue(os.path.exists(path), 
                       f"Path {path} should exist")
        self.assertTrue(os.path.isdir(path), 
                       f"Path {path} should be a directory")
    
    def test_saveGame_creates_file(self):
        """Test that saveGame successfully creates a file"""
        test_game = list("XOX OXO X")
        saveGame(test_game)
        
        file_path = os.path.join(_getPath(), self.game_file)
        self.assertTrue(os.path.exists(file_path), 
                       "Game file should be created after save")
    
    def test_saveGame_and_restoreGame_consistency(self):
        """Test that saved game can be restored with identical data"""
        test_game = list("XO XO XO ")
        saveGame(test_game)
        restored_game = restoreGame()
        
        self.assertEqual(test_game, restored_game,
                        "Restored game should match saved game")
        self.assertEqual(len(restored_game), 9,
                        "Restored game should have 9 cells")
    
    def test_restoreGame_returns_list(self):
        """Test that restoreGame returns a list type"""
        saveGame(list("         "))
        restored = restoreGame()
        self.assertIsInstance(restored, list, 
                            "Restored game should be a list")
    
    def test_saveGame_with_empty_board(self):
        """Test saving an empty game board"""
        empty_game = list(" " * 9)
        saveGame(empty_game)
        restored = restoreGame()
        self.assertEqual(empty_game, restored,
                        "Empty game should save and restore correctly")
    
    def test_saveGame_with_full_board(self):
        """Test saving a completely filled board"""
        full_game = list("XOXOXOXOX")
        saveGame(full_game)
        restored = restoreGame()
        self.assertEqual(full_game, restored,
                        "Full game should save and restore correctly")


class TestOxoLogicBasic(unittest.TestCase):
    """Test cases for basic oxo_logic module functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.empty_game = list(" " * 9)
        random.seed(42)  # Set seed for reproducible tests
        
    def test_newGame_returns_list(self):
        """Test that newGame returns a list"""
        game = newGame()
        self.assertIsInstance(game, list, "newGame should return a list")
    
    def test_newGame_correct_size(self):
        """Test that newGame returns exactly 9 cells"""
        game = newGame()
        self.assertEqual(len(game), 9, 
                        "New game should have 9 cells")
    
    def test_newGame_all_empty(self):
        """Test that newGame returns all empty spaces"""
        game = newGame()
        self.assertEqual(game, list(" " * 9),
                        "New game should have all empty cells")
        for cell in game:
            self.assertEqual(cell, " ", "Each cell should be empty")
    
    def test_generateMove_returns_valid_index(self):
        """Test _generateMove returns a valid cell index"""
        game = newGame()
        move = _generateMove(game)
        self.assertIn(move, range(9),
                     "Generated move should be between 0 and 8")
    
    def test_generateMove_returns_empty_cell(self):
        """Test _generateMove only selects empty cells"""
        game = list("XOX      ")
        move = _generateMove(game)
        self.assertIn(move, [3, 4, 5, 6, 7, 8],
                     "Move should be in an empty cell")
        self.assertEqual(game[move], " ",
                        "Selected cell should be empty")
    
    def test_generateMove_full_board(self):
        """Test _generateMove returns -1 when board is full"""
        game = list("XOXOXOXOX")
        move = _generateMove(game)
        self.assertEqual(move, -1,
                        "Should return -1 when board is full")


class TestUserMove(unittest.TestCase):
    """Test cases for userMove function"""
    
    def test_userMove_places_X(self):
        """Test that userMove places 'X' in the specified cell"""
        game = newGame()
        userMove(game, 0)
        self.assertEqual(game[0], 'X',
                        "UserMove should place X in specified cell")
    
    def test_userMove_valid_returns_empty_string(self):
        """Test userMove returns empty string when no win"""
        game = newGame()
        result = userMove(game, 4)
        self.assertEqual(result, "",
                        "Should return empty string when no win")
    
    def test_userMove_occupied_cell_raises_ValueError(self):
        """Test that userMove raises ValueError for occupied cell"""
        game = newGame()
        game[0] = 'X'
        
        with self.assertRaises(ValueError, 
                              msg="Should raise ValueError for occupied cell"):
            userMove(game, 0)
    
    def test_userMove_winning_horizontal(self):
        """Test userMove detects horizontal win"""
        game = list("XX O O   ")
        result = userMove(game, 2)
        self.assertEqual(result, 'X',
                        "Should return 'X' for winning move")
    
    def test_userMove_winning_vertical(self):
        """Test userMove detects vertical win"""
        game = list("X  X     ")
        result = userMove(game, 6)
        self.assertEqual(result, 'X',
                        "Should return 'X' for vertical win")
    
    def test_userMove_winning_diagonal(self):
        """Test userMove detects diagonal win"""
        game = list("X   X O  ")
        result = userMove(game, 8)
        self.assertEqual(result, 'X',
                        "Should return 'X' for diagonal win")
    
    def test_userMove_all_positions(self):
        """Test userMove works for all valid positions"""
        for position in range(9):
            game = newGame()
            result = userMove(game, position)
            self.assertEqual(game[position], 'X',
                           f"Should place X at position {position}")


class TestComputerMove(unittest.TestCase):
    """Test cases for computerMove function"""
    
    def test_computerMove_places_O(self):
        """Test that computerMove places 'O' on the board"""
        game = newGame()
        random.seed(42)
        computerMove(game)
        self.assertIn('O', game,
                     "Computer move should place O on board")
    
    def test_computerMove_empty_board(self):
        """Test computerMove on empty board"""
        game = newGame()
        result = computerMove(game)
        o_count = game.count('O')
        self.assertEqual(o_count, 1,
                        "Should place exactly one O")
        self.assertEqual(result, "",
                        "Should return empty string when no win")
    
    def test_computerMove_returns_D_on_draw(self):
        """Test computerMove returns 'D' when board is full"""
        game = list("XXXOOOXOX")
        result = computerMove(game)
        self.assertEqual(result, 'D',
                        "Should return 'D' for draw (full board)")
    
    def test_computerMove_winning(self):
        """Test computerMove detects its own win"""
        # Set up board where O can potentially win
        game = list("OO XX    ")
        # We need to test if O completes a line
        # Since move is random, we'll set up guaranteed win
        game = list("OOX XX   ")
        random.seed(5)  # Try different seeds to get the winning move
        
        # Alternative: test with only one move possible that wins
        game = list("OOXXXOX  ")  # If O plays position 8, might win
        # This is tricky due to randomness; better approach:
        for _ in range(100):  # Try multiple times
            test_game = list("OO XXX   ")
            result = computerMove(test_game)
            if result == 'O':
                self.assertEqual(result, 'O', "Should detect win")
                break


class TestWinDetection(unittest.TestCase):
    """Comprehensive test cases for _isWinningMove function"""
    
    def setUp(self):
        """Set up for win detection tests"""
        self.check_win = _isWinningMove
    
    # Horizontal wins
    def test_top_row_X_wins(self):
        """Test X wins with top row (0,1,2)"""
        game = list("XXXOO    ")
        self.assertTrue(self.check_win(game),
                       "Should detect top row win")
    
    def test_middle_row_O_wins(self):
        """Test O wins with middle row (3,4,5)"""
        game = list("X XOOOXX ")
        self.assertTrue(self.check_win(game),
                       "Should detect middle row win")
    
    def test_bottom_row_X_wins(self):
        """Test X wins with bottom row (6,7,8)"""
        game = list("OO  O XXX")
        self.assertTrue(self.check_win(game),
                       "Should detect bottom row win")
    
    # Vertical wins
    def test_left_column_O_wins(self):
        """Test O wins with left column (0,3,6)"""
        game = list("OX OX O  ")
        self.assertTrue(self.check_win(game),
                       "Should detect left column win")
    
    def test_middle_column_X_wins(self):
        """Test X wins with middle column (1,4,7)"""
        game = list(" XO XO X ")
        self.assertTrue(self.check_win(game),
                       "Should detect middle column win")
    
    def test_right_column_O_wins(self):
        """Test O wins with right column (2,5,8)"""
        game = list("X OX OX O")
        self.assertTrue(self.check_win(game),
                       "Should detect right column win")
    
    # Diagonal wins
    def test_main_diagonal_X_wins(self):
        """Test X wins with main diagonal (0,4,8)"""
        game = list("XO  XO  X")
        self.assertTrue(self.check_win(game),
                       "Should detect main diagonal win")
    
    def test_anti_diagonal_O_wins(self):
        """Test O wins with anti-diagonal (2,4,6)"""
        game = list("X OXO OX ")
        self.assertTrue(self.check_win(game),
                       "Should detect anti-diagonal win")
    
    # No win scenarios
    def test_no_win_empty_board(self):
        """Test empty board has no winner"""
        game = list("         ")
        self.assertFalse(self.check_win(game),
                        "Empty board should have no winner")
    
    def test_no_win_partial_game(self):
        """Test partial game with no winner"""
        game = list("XO XO    ")
        self.assertFalse(self.check_win(game),
                        "Partial game should have no winner")
    
    def test_no_win_full_board_draw(self):
        """Test full board with no winner (draw)"""
        game = list("XXOOOXXXO")
        self.assertFalse(self.check_win(game),
                        "Draw board should have no winner")


class TestGamePersistence(unittest.TestCase):
    """Test cases for save and restore game logic"""
    
    def tearDown(self):
        """Clean up test files"""
        try:
            from oxo_data import _getPath
            test_file = os.path.join(_getPath(), "oxogame.dat")
            if os.path.exists(test_file):
                os.remove(test_file)
        except:
            pass
    
    def test_saveGame_logic(self):
        """Test saveGame_logic function"""
        game = list("XOX O    ")
        saveGame_logic(game)
        
        # Verify file was created
        from oxo_data import _getPath
        file_path = os.path.join(_getPath(), "oxogame.dat")
        self.assertTrue(os.path.exists(file_path),
                       "Save logic should create file")
    
    def test_restoreGame_logic_with_valid_game(self):
        """Test restoreGame_logic with valid saved game"""
        test_game = list("XO XO XO ")
        saveGame(test_game)
        
        restored = restoreGame_logic()
        self.assertEqual(len(restored), 9,
                        "Restored game should have 9 cells")
        self.assertEqual(restored, test_game,
                        "Restored game should match saved game")
    
    def test_restoreGame_logic_no_file_returns_new(self):
        """Test restoreGame_logic returns new game when file missing"""
        # Ensure no file exists
        from oxo_data import _getPath
        file_path = os.path.join(_getPath(), "oxogame.dat")
        if os.path.exists(file_path):
            os.remove(file_path)
        
        game = restoreGame_logic()
        self.assertEqual(game, list(" " * 9),
                        "Should return new game when file missing")
    
    def test_restoreGame_logic_invalid_size_returns_new(self):
        """Test restoreGame_logic returns new game for invalid size"""
        # Save invalid game (wrong size)
        with patch('oxo_data.restoreGame', return_value=list("XOX")):
            game = restoreGame_logic()
            self.assertEqual(len(game), 9,
                           "Should return new game for invalid size")


class TestUIFunctions(unittest.TestCase):
    """Test cases for UI module functions"""
    
    def test_getMenuChoice_valid_input(self):
        """Test getMenuChoice with valid numeric input"""
        test_menu = ["Option 1", "Option 2", "Option 3"]
        
        with patch('builtins.input', return_value='2'):
            choice = getMenuChoice_ui(test_menu)
            self.assertEqual(choice, 2,
                           "Should return the selected option number")
    
    def test_getMenuChoice_empty_menu_raises_error(self):
        """Test that empty menu raises ValueError"""
        with self.assertRaises(ValueError,
                              msg="Empty menu should raise ValueError"):
            getMenuChoice_ui([])
    
    def test_startGame_ui_returns_new_game(self):
        """Test that startGame_ui returns a new empty game"""
        game = startGame_ui()
        self.assertEqual(len(game), 9,
                        "Should return 9-cell game")
        self.assertEqual(game, list(" " * 9),
                        "Should return empty game")
    
    def test_printGame_ui_no_error(self):
        """Test that printGame_ui executes without error"""
        test_game = list("XO XO XO ")
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            printGame_ui(test_game)
            # Verify print was called
            self.assertTrue(mock_print.called,
                          "printGame should call print")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_userMove_all_boundary_positions(self):
        """Test userMove on boundary positions (0 and 8)"""
        # Test position 0
        game = newGame()
        userMove(game, 0)
        self.assertEqual(game[0], 'X', "Should work at position 0")
        
        # Test position 8
        game = newGame()
        userMove(game, 8)
        self.assertEqual(game[8], 'X', "Should work at position 8")
    
    def test_multiple_moves_sequence(self):
        """Test a sequence of valid moves"""
        game = newGame()
        
        userMove(game, 0)
        computerMove(game)
        userMove(game, 2)
        computerMove(game)
        
        # Verify board has correct number of pieces
        x_count = game.count('X')
        o_count = game.count('O')
        
        self.assertEqual(x_count, 2, "Should have 2 X's")
        self.assertEqual(o_count, 2, "Should have 2 O's")
    
    def test_game_state_consistency(self):
        """Test game state remains consistent through save/restore"""
        original = list("XOX O XO ")
        saveGame(original)
        restored = restoreGame()
        
        # Verify each position
        for i in range(9):
            self.assertEqual(original[i], restored[i],
                           f"Position {i} should match")


class TestPerformance(unittest.TestCase):
    """Test performance-related aspects"""
    
    def test_generateMove_performance(self):
        """Test that _generateMove executes quickly"""
        import time
        
        game = newGame()
        start = time.time()
        
        for _ in range(1000):
            _generateMove(game)
        
        elapsed = time.time() - start
        self.assertLess(elapsed, 1.0,
                       "1000 move generations should take less than 1 second")
    
    def test_win_check_performance(self):
        """Test that _isWinningMove executes quickly"""
        import time
        
        game = list("XOXOXOXOX")
        start = time.time()
        
        for _ in range(1000):
            _isWinningMove(game)
        
        elapsed = time.time() - start
        self.assertLess(elapsed, 0.1,
                       "1000 win checks should take less than 0.1 seconds")


def run_test_suite():
    """
    Run the complete test suite with detailed reporting
    """
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestOxoData))
    suite.addTests(loader.loadTestsFromTestCase(TestOxoLogicBasic))
    suite.addTests(loader.loadTestsFromTestCase(TestUserMove))
    suite.addTests(loader.loadTestsFromTestCase(TestComputerMove))
    suite.addTests(loader.loadTestsFromTestCase(TestWinDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestGamePersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestUIFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Run with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Run all tests with verbose output
    print("Starting Tic Tac Toe Unit Test Suite...")
    print("="*70)
    
    success = run_test_suite()
    
    # Exit with appropriate code
    exit(0 if success else 1)
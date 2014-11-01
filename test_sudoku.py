import random
import unittest
from sudoku import Puzzle
from sudoku import Grid

class TestSudoku(unittest.TestCase):
  
  maxDiff = None

  def setUp(self):
    self.solved_grid = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
      [4, 5, 6, 7, 8, 9, 1, 2, 3],
      [7, 8, 9, 1, 2, 3, 4, 5, 6],
      [3, 4, 5, 9, 6, 7, 8, 1, 2],
      [8, 1, 2, 3, 4, 5, 9, 6, 7],
      [9, 6, 7, 8, 1, 2, 3, 4, 5],
      [2, 3, 1, 5, 9, 4, 6, 7, 8],
      [5, 9, 4, 6, 7, 8, 2, 3, 1],
      [6, 7, 8, 2, 3, 1, 5, 9, 4]]

    self.easy_grid = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
      [4, 0, 6, 7, 8, 9, 1, 2, 3],
      [7, 8, 9, 1, 2, 3, 4, 5, 6],
      [3, 4, 5, 9, 6, 7, 8, 1, 2],
      [8, 1, 2, 3, 4, 5, 9, 6, 0],
      [9, 6, 7, 8, 1, 2, 3, 4, 5],
      [2, 3, 1, 5, 9, 4, 6, 7, 8],
      [5, 9, 4, 6, 7, 8, 2, 3, 1],
      [6, 7, 8, 2, 0, 1, 5, 9, 4]]

    self.unsolvable_grid = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
      [4, 0, 6, 7, 8, 9, 1, 2, 3],
      [7, 1, 9, 1, 2, 3, 4, 5, 6],
      [3, 4, 5, 9, 6, 7, 8, 1, 2],
      [8, 1, 2, 3, 4, 5, 9, 6, 0],
      [9, 6, 7, 8, 1, 9, 3, 4, 5],
      [2, 3, 1, 5, 9, 4, 6, 7, 8],
      [5, 5, 4, 6, 7, 8, 2, 3, 1], 
      [6, 7, 8, 2, 0, 1, 5, 9, 4]]

    self.second_easy = [[5, 0, 3, 0, 1, 0, 4, 0, 7],
      [0, 0, 0, 0, 8, 0, 9, 0, 0],
      [0, 0, 4, 0, 5, 3, 0, 2, 6],
      [6, 0, 0, 0, 0, 0, 2, 5, 0],
      [0, 2, 0, 9, 7, 5, 0, 6, 0],
      [0, 3, 5, 0, 0, 0, 0, 0, 4],
      [2, 8, 0, 4, 9, 0, 5, 0, 0],
      [0, 0, 6, 0, 2, 0, 0, 0, 0],
      [1, 0, 9, 0, 3, 0, 6, 0, 2]]

	# test that a puzzle grid is successfully populated using the constructor
  def test_puzzle_constructor_successful(self):
		puzzle = Grid(self.solved_grid)
		self.assertEqual(puzzle.grid[0], [1, 2, 3, 4, 5, 6, 7, 8, 9])
		self.assertEqual(puzzle.grid[1], [4, 5, 6, 7, 8, 9, 1, 2, 3])
		self.assertEqual(puzzle.grid[2], [7, 8, 9, 1, 2, 3, 4, 5, 6])
		self.assertEqual(puzzle.grid[3], [3, 4, 5, 9, 6, 7, 8, 1, 2])
		self.assertEqual(puzzle.grid[4], [8, 1, 2, 3, 4, 5, 9, 6, 7])
		self.assertEqual(puzzle.grid[5], [9, 6, 7, 8, 1, 2, 3, 4, 5])
		self.assertEqual(puzzle.grid[6], [2, 3, 1, 5, 9, 4, 6, 7, 8])
		self.assertEqual(puzzle.grid[7], [5, 9, 4, 6, 7, 8, 2, 3, 1])
		self.assertEqual(puzzle.grid[8], [6, 7, 8, 2, 3, 1, 5, 9, 4])

	# test retrieving an individual space
  def test_space_retrieval(self):
		puzzle = Grid(self.solved_grid)
		self.assertEqual(puzzle.space(1, 2), 6)
		self.assertEqual(puzzle.space(7, 8), 1)
		self.assertEqual(puzzle.space(4, 4), 4)
		self.assertEqual(puzzle.space(0, 0), 1)
		self.assertEqual(puzzle.space(8, 8), 4)

	# test that retrieving a false space errors
  def test_space_retrieval_errors(self):
		puzzle = Grid(self.solved_grid)
		self.assertFalse(puzzle.space(9, 0))

	# test that sections can be retrieved
  def test_section_retrieval(self):
		puzzle = Grid(self.solved_grid)
		self.assertEqual(puzzle.section(0, 0), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
		self.assertEqual(puzzle.section(3, 3), [[9, 6, 7], [3, 4, 5], [8, 1, 2]])

	# test that non existant sections cannot be retrieved
  def test_section_retrieval_errors(self):
    puzzle = Grid(self.solved_grid)
    self.assertFalse(puzzle.section(0, 9))
    self.assertFalse(puzzle.section(-1, 0))
    self.assertFalse(puzzle.section(9, 9))
    self.assertFalse(puzzle.section(-1, -1))

	# test that invidiual lines can be retrieved
  def test_line_retrieval(self):
		puzzle = Grid(self.solved_grid)
		self.assertEqual(puzzle.line(1), [4, 5, 6, 7, 8, 9, 1, 2, 3])

	# test that non existent lines cannot be retrieved
  def test_line_retrieval_errors(self):
		puzzle = Grid(self.solved_grid)
		self.assertFalse(puzzle.line(9))

  # test that vertical lines can be retrieved
  def test_vertical_line_retrieval(self):
    puzzle = Grid(self.solved_grid)
    self.assertEqual(puzzle.vertical_line(1), [2, 5, 8, 4, 1, 6, 3, 9, 7])

  # test that non existent lines cannot be retrieved
  def test_vertical_line_retrieval_errors(self):
    puzzle = Grid(self.solved_grid)
    self.assertFalse(puzzle.line(9))

	# test that a completed puzzle is detected correctly
  def test_puzzle_complete(self):
		puzzle = Grid(self.solved_grid)
		self.assertTrue(puzzle.is_completed())

	# test that a puzzle that has not been properly solved is detected
  def test_puzzle_incorrectly_completed(self):
		puzzle = Grid([[1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [3, 4, 5, 9, 6, 7, 8, 1, 2],
    [8, 1, 2, 3, 4, 5, 9, 6, 7],
    [9, 6, 7, 8, 1, 2, 3, 4, 5],
    [2, 3, 1, 5, 9, 4, 6, 7, 8],
    [5, 9, 4, 6, 7, 8, 2, 3, 1], 
    [6, 7, 8, 2, 3, 1, 5, 9, 1]])
		self.assertFalse(puzzle.is_completed())

	# test that a completed line is accurate
  def test_completed_line_accuracy(self):
		puzzle = Puzzle(self.easy_grid)
		puzzle.solve()
		self.assertEqual(puzzle.grid.line(1), [4, 5, 6, 7, 8, 9, 1, 2, 3])

	# test that a completed section is accurate
  def test_completed_section_accuracy(self):
		puzzle = Puzzle(self.easy_grid)
		puzzle.solve()
		self.assertEqual(puzzle.grid.section(0, 0), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

  def test_solve_space(self):
    puzzle = Grid(self.easy_grid)
    puzzle.solve_space(1, 1, 5)
    puzzle.solve_space(8, 4, 3)
    puzzle.solve_space(4, 8, 7)
    self.assertEquals(puzzle.grid, self.solved_grid)

	# test that an unsolvable puzzle is returned as false
  def test_unsolvable_puzzle(self):
		puzzle = Puzzle(self.unsolvable_grid)
		self.assertFalse(puzzle.solve())
	
  # test that a grid with an empty space is returned as unsolvable
  def test_unsolvable_grid(self):
    puzzle = Grid(self.unsolvable_grid)
    self.assertFalse(puzzle.is_solvable())

  def test_possible_space_solutions(self):
    puzzle = Grid(self.easy_grid)
    self.assertEqual(puzzle.determine_possible_spaces(1, 1), [5])
    self.assertEqual(puzzle.determine_possible_spaces(8, 4), [3])
    puzzle_two = Grid(self.second_easy)
    self.assertEqual(puzzle_two.determine_possible_spaces(1, 1), [1, 6, 7])
    self.assertEqual(puzzle_two.determine_possible_spaces(7, 5), [1, 7, 8])

  def test_possible_space_errors(self):
    puzzle = Grid(self.easy_grid)
    self.assertTrue(puzzle.determine_possible_spaces(1, 2))

  def test_finding_all_possiblities_for_all_spaces(self):
    puzzle = Grid(self.second_easy)
    self.assertEquals(puzzle.find_all_possibilities(), {(0, 1): [6, 9], (0, 3): [2, 6], (0, 5): [2, 6, 9], (0, 7): [8],
                                                        (1, 0): [7], (1, 1): [1, 6, 7], (1, 2): [1, 2, 7], (1, 3): [2, 6, 7], (1, 5): [2, 4, 6, 7], (1, 7): [1, 3], (1, 8): [1, 3, 5],
                                                        (2, 0): [7, 8, 9], (2, 1): [1, 7, 9], (2, 3): [7], (2, 6): [1, 8],
                                                        (3, 1): [1, 4, 7, 9], (3, 2): [1, 7, 8], (3, 3): [1, 3, 8], (3, 4): [4], (3, 5): [1, 4, 8], (3, 8): [1, 3, 8, 9],
                                                        (4, 0): [4, 8], (4, 2): [1, 8], (4, 6): [1, 3, 8], (4, 8): [1, 3, 8],
                                                        (5, 0): [7, 8, 9], (5, 3): [1, 2, 6, 8], (5, 4): [6], (5, 5): [1, 2, 6, 8], (5, 6): [1, 7, 8], (5, 7): [1, 7, 8, 9],
                                                        (6, 2): [7], (6, 5): [1, 6, 7], (6, 7): [1, 3, 7], (6, 8): [1, 3],
                                                        (7, 0): [3, 4, 7], (7, 1): [4, 5, 7], (7, 3): [1, 5, 7, 8], (7, 5): [1, 7, 8], (7, 6): [1, 3, 7, 8], (7, 7): [1, 3, 4, 7, 8, 9], (7, 8): [1, 3, 8, 9],
                                                        (8, 1): [4, 5, 7], (8, 3): [5, 7, 8], (8, 5): [7, 8], (8, 7): [4, 7, 8]})

  def test_complete_list(self):
    puzzle = Grid([])
    self.assertTrue(puzzle.is_complete_sequence([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    self.assertFalse(puzzle.is_complete_sequence([1, 2, 3, 4, 5, 6, 7, 8]))
    self.assertTrue(puzzle.is_complete_sequence([9, 8, 7, 6, 5, 4, 3, 2, 1]))
    self.assertFalse(puzzle.is_complete_sequence([2, 1, 5, 4, 5, 3, 7, 8, 9]))

  def test_solve_easy(self):
    puzzle = Puzzle(self.easy_grid)
    solution = puzzle.solve()
    self.assertEquals(solution.grid, self.solved_grid)

  def test_solve_second_easy(self):
    puzzle = Puzzle(self.second_easy)
    solution = puzzle.solve()
    self.assertEquals(solution.grid, self.solved_grid)

if __name__ == '__main__':
    unittest.main()
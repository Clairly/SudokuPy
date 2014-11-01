import itertools
from sets import Set
import Queue

class Grid(object):
  def __init__(self, grid):
    super(Grid, self).__init__()
    self.grid = grid

  def space(self, x, y):
    if x < 0 or x > 8 or y < 0 or y > 8:
      return False
    return self.grid[x][y]

  def line(self, x):
    if x < 0 or x > 8:
      return False;
    return self.grid[x]

  def section(self, x, y):
    if x < 0 or x > 8 or y < 0 or y > 8:
      return False

    if x in range(0, 3):
      x_range = range(0, 3);
    elif x in range(3, 6):
      x_range = range(3, 6)
    elif x in range(6, 9):
      x_range = range(6, 9)

    if y in range(0, 3):
      y_range = range(0, 3)
    elif y in range(3, 6):
      y_range = range(3, 6)
    elif y in range(6, 9):
      y_range = range(6, 9)

    mini_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    
    x = 0
    for i in x_range:
      y = 0
      for j in y_range:
        mini_grid[x][y] = self.grid[i][j]
        y += 1
      x += 1

    return mini_grid

  def vertical_line(self, y):
    if y < 0 or y > 8:
      return False;
    line = []
    for x in range(0, 9):
      line.append(self.grid[x][y])
    return line 

  def determine_possible_spaces(self, x, y):
    if self.space(x, y) != 0: return True

    possibles = Set(range(1, 10))

    horizontal_set = Set(self.line(x))
    vertical_set = Set(self.vertical_line(y))
    section_set = Set(list(itertools.chain(*self.section(x, y))))

    possibles = possibles - horizontal_set - vertical_set - section_set

    possibles = sorted(list(possibles))

    return possibles

  def find_all_possibilities(self):
    # first look for all empty spaces
    # when one is found, find its possibile entries
    # and add each entry to the dictionary
    all_possibles = {}
    for x in range(0, 9):
      for y in range(0, 9):
        if self.space(x, y) == 0:
          all_possibles[x, y] = self.determine_possible_spaces(x, y)
    return all_possibles

  def is_solvable(self):
    '''returns True if every open space has at least one possible state,
      returns False if one space is not'''
    for x in range(0, 9):
      for y in range(0, 9):
        if self.space(x, y) == 0 and len(self.determine_possible_spaces(x, y)) == 0: return False
    return True

  def is_complete_sequence(self, line):
    if len(line) != 9: return False

    # sort list
    new_line = sorted(line)

    x = 1
    for i in new_line:
      if i != x: return False
      x = x + 1
    return True

  def is_completed(self):
    # first verify each space has an answer
    for x in range(0, 9):
      for y in range(0, 9):
        if self.space(x, y) == 0: return False

    #verify each vertical line, horizontal line, and section go from 1-9 with no repetition
    for y in range(0, 9):
      if self.is_complete_sequence(self.vertical_line(y)) == False: 
        #print "vertical line ", y, " is incorrect"
        return False
    for x in range(0, 9):
      if self.is_complete_sequence(self.line(x)) == False: 
        # print "horizontal line ", x, " is incorrect"
        return False
    for x in range(0, 3):
      x = x * 3
      for y in range(0, 3):
        y = y * 3
        flatten_section = list(itertools.chain(*self.section(x, y)))
        if self.is_complete_sequence(flatten_section) == False: 
          # print "section ", x, ", ", y, " is incorrect"
          # print self.section(x, y)
          return False

    return True

  def priority(self):
    num = 0
    possibles = self.find_all_possibilities()
    for space in possibles:
      num = num + len(space)
    return num

  def solve_space(self, x, y, num):
    if self.space(x, y) == 0: self.grid[x][y] = num


class Puzzle(object):
  """docstring for Puzzle"""
  def __init__(self, grid):
    super(Puzzle, self).__init__()
    self.grid = Grid(grid)
    self.possible_states = Queue.PriorityQueue()
    self.possible_states.put((self.grid.priority(), self.grid))
    self.visited_grids = []

  def solve(self):
    # only try to solve if it's not already completed and there are still possible grids to examine
    while self.possible_states.empty() != True:
      # pop off first item in priority queue and add it to visited grids
      current_priority, current_grid = self.possible_states.get()
      
      # if the current grid has not already been examined:
      if current_grid in self.visited_grids: break  

      # return current grid if solved successfully 
      if current_grid.is_completed(): return current_grid

      self.visited_grids.append(current_grid)

      print current_grid.grid
      # get all space options for this grid
      # if there are no options, this grid is not feasible; move on to the next one
      options = current_grid.find_all_possibilities()
      if len(options) == 0: break
      
      # create a new grid for each possibility in each open space by:

      # order the options by the lowest number of choices per square
      for space in sorted(options, key=lambda k: len(options[k]), reverse=True):

        x, y = space
        
        # create a new grid for each number possible in that space
        for number_available in current_grid.determine_possible_spaces(x, y):
          new_grid = Grid(current_grid.grid)
          new_grid.solve_space(x, y, number_available)
          
          # check that the new grid is not in the visited list or in the priority queue or unsolvable
          if new_grid in self.visited_grids or new_grid.is_solvable == False: #TODO or new_grid in self.possible_states.items():
            break
          
          # add grid to priority queue (priority=total number of possibilities for all open spaces, object=grid)
          self.possible_states.put((new_grid.priority(), new_grid))

    return False
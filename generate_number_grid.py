import random

"""
This file contains the class used for generation of a grid of numbers such that
each row and column contains one of each number from 1 to sz

This is accomplished using backtracking
"""


class KenKenGrid:
    stack = []
    grid = []

    """
    Upon initialisation, generates the top level node with an empty grid (all zeroes)
    
    sz: defines the height and width of the grid
    """

    def __init__(self, sz):
        self.sz = sz
        hold = [0] * sz
        for i in range(sz):
            self.grid.append(hold.copy())
        self.stack.append(NumberGridGenerationBackTrackNode(self.grid, sz=sz))

    """
    Uses backtracking algorithm techniques to randomly generate a valid grid
    """

    def generate_random_grid(self):
        while len(self.stack) > 0:
            # Peeks at the top node
            node = self.stack[len(self.stack) - 1]

            # If the nodes current position variable is None, this means the node has successfully inserted a value
            # at every point on the grid.
            if node.position is None:
                return node.grid

            # Calls a method on the top level node to see if any values can possibly be placed at the current position
            next_value = node.pop_possible_value()
            if next_value is None:
                # If no values can be placed at this position, the current node is a dead end. Pop off stack.
                self.stack.pop()
            else:
                # Otherwise, push a new node to the top of the stack with the value updated at this position
                hold_grid = node.grid.copy()
                hold_grid[node.position[0]][node.position[1]] = next_value
                self.stack.append(NumberGridGenerationBackTrackNode(hold_grid,  self.sz, node.get_appended_position()))
        return None


"""
This class represents a single node used in this backtracking algorithm
"""


class NumberGridGenerationBackTrackNode:
    def __init__(self, grid, sz, position=(0, 0)):
        self.sz = sz
        self.position = position
        self.grid = grid
        self.possible_values = self.get_possible_values()

    """
    Returns the next position to check in order after the current position.
    If the current position is the last position to check, return None
    """

    def get_appended_position(self):
        if self.position[1] != (self.sz - 1):
            return self.position[0], self.position[1] + 1
        elif self.position[0] != (self.sz - 1):
            return self.position[0] + 1, 0
        else:
            return None

    # Returns all possible values for the current position based on the conditions
    def get_possible_values(self):
        if self.position is None:
            return []

        # Hold initially stores every possible number from 1 to sz
        hold = [x + 1 for x in range(self.sz)]

        # Iterates over the row and column the current position resides in
        # Removes any value from hold that it comes across
        for i in range(self.sz):
            if i != self.position[1]:
                value = self.grid[self.position[0]][i]
                if value in hold:
                    hold.remove(value)
            if i != self.position[0]:
                value = self.grid[i][self.position[1]]
                if value in hold:
                    hold.remove(value)

        # Shuffles the remaining contents of hold
        random.shuffle(hold)
        return hold

    # From the valid possible number values for the current position, pops to top one
    def pop_possible_value(self):
        if len(self.possible_values) != 0:
            return self.possible_values.pop()
        else:
            return None

import random
import itertools

"""
This file contains the Block object which represents each block of the KenKen board.
It generates blocks by attempting to add a neighbouring position to it at each iteration
"""

class Block:
    positions = []
    sign = None
    value = 0

    def __init__(self, init, sz):
        self.positions = []
        self.positions.append(init)
        self.sz = sz

    """
    Appends a new position to the block
    """
    def add_new_tile(self, pos):
        self.positions.append(pos)

    """
    Returns an available neighbouring position.
    Returns None if not possible
    """
    def get_possible_next_position(self, available_positions):
        random.shuffle(self.positions)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)

        for pos in self.positions:
            for direction in directions:
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                # Checks this new position is not outside board constraints
                if 0 <= pos[0] <= self.sz - 1 and 0 <= pos[1] <= self.sz - 1:
                    # Checks this position is available for use, and is not already in the block
                    if new_pos not in self.positions and new_pos in available_positions:
                        return new_pos
        return None

    """
    Calculates the value of the block if the plus sign was assigned to this block
    """
    def calculate_plus(self, number_grid):
        if len(self.positions) == 1:
            return None
        value = 0
        for pos in self.positions:
            value += number_grid[pos[0]][pos[1]]

        self.sign = "+"
        self.value = value
        return value

    """
    Calculates the value of the block if the multiplication sign was assigned to this block
    """
    def calculate_multiply(self, number_grid):
        if len(self.positions) == 1:
            return None
        value = 1
        for pos in self.positions:
            value *= number_grid[pos[0]][pos[1]]

        self.sign = "*"
        self.value = value
        return value

    """
    Calculates the value of the block if the minus sign was assigned to this block
    """
    def calculate_minus(self, number_grid):
        if len(self.positions) == 1:
            return None
        vs = []
        for pos in self.positions:
            vs.append(number_grid[pos[0]][pos[1]])

        vs.sort(reverse=True)
        v = vs[0]
        del vs[0]
        for x in vs:
            v -= x

        # Checks the result is positive
        if v > 0:
            self.sign = "-"
            self.value = v
            return v
        else:
            return None

    """
    Calculates the value of the block if the divide sign was assigned to this block
    """
    def calculate_divide(self, number_grid):
        if len(self.positions) != 2:
            return None
        v1 = number_grid[self.positions[0][0]][self.positions[0][1]]
        v2 = number_grid[self.positions[1][0]][self.positions[1][1]]
        v = v2/v1 if v2>v1 else v1/v2

        # Checks that the result is an integer
        if v - int(v) == 0:
            self.sign = "/"
            self.value = v
            return v
        else:
            return None

    """
    Calculates and returns all possible permutations for the block given the board
    """
    def calculate_all_possible_sets(self, grid):
        n = len(self.positions)
        tile_number_possibilities = []
        possible_sets = []

        # Firstly determines what values are possible based on surrounding blocks and tiles
        for pos in self.positions:
            hold = [x + 1 for x in range(self.sz)]

            # Removes any numbers from the hold list that already exist on the same row and column as the current pos
            for i in range(self.sz):
                if grid[pos[0]][i] in hold:
                    hold.remove(grid[pos[0]][i])
                if grid[i][pos[1]] in hold:
                    hold.remove(grid[i][pos[1]])
            tile_number_possibilities.append(hold)
        # Generates a list of all possible permutation of numbers given the possible numbers for each tile
        tile_number_possibilities_sets = list(itertools.product(*tile_number_possibilities))

        # Next up calculates the possible permutations of N numbers given the sign and value
        if self.sign is None:
            return self.value
        # If +, determines all possible permutations given all numbers less than the value
        # If there are more than 2 tiles in this block, remove more values from the end of the list
        # (since each tile must at least equal 1). Then only keep permutations that sum to value
        if self.sign == "+":
            possible_numbers = [x+1 for x in range(self.sz) if x+1 < (self.value - (n - 2))]
            possible_sets = list(itertools.combinations_with_replacement(possible_numbers,n))
            possible_sets = [t for t in possible_sets if sum(t) == self.value]
        # If -, simply find all permutations of all numbers from 1->sz where the outcome is value
        if self.sign == "-":
            possible_numbers = [x + 1 for x in range(self.sz)]
            possible_sets = list(itertools.combinations_with_replacement(possible_numbers, n))
            possible_sets = [t for t in possible_sets if max(t) - (sum(t) - max(t)) == self.value]
        # If /, determine all factors of value in the list of numbers from 1->sz
        # Determine all permutation pairs of these numbers, and keep any where the outcome is value
        if self.sign == "/":
            possible_numbers = [x + 1 for x in range(self.sz) if self.value % (x + 1) == 0]
            possible_sets = list(itertools.combinations_with_replacement(possible_numbers, n))
            possible_sets = [t for t in possible_sets if max(t) / min(t) == self.value and (max(t) / min(t)) - int(max(t) / min(t)) == 0]
        # If *, determine all factors of value in the list of numbers from 1->sz
        # Determine all permutations of these numbers, and keep any where the product is value
        if self.sign == "*":
            possible_numbers = [x + 1 for x in range(self.sz) if self.value % (x+1) == 0]
            possible_sets = list(itertools.combinations_with_replacement(possible_numbers, n))
            possible_sets = [t for t in possible_sets if self.product(t) == self.value]

        # With these 2 lists of permutations, find the intersection (IE the list of values that are common to both)
        same = self.intersection_of_tiles_and_possible_sets(possible_sets, tile_number_possibilities_sets)
        if len(same) == 1:
            return [True]*len(self.positions)
        elif len(same) > 1:
            len_check = [len(x) == 1 for x in tile_number_possibilities]
            print(tile_number_possibilities, same)
            return len_check
        else:
            return [False]*len(self.positions)

    """
    Setters
    """
    def set_sign(self, sign):
        self.sign = sign

    def set_value(self, value):
        self.value = value

    def reset_value_and_sign(self):
        self.sign = None
        self.value = 0

    # Finds the intersection of the 2 lists of permutations
    @staticmethod
    def intersection_of_tiles_and_possible_sets(possible_sets, tile_number_possibilities):
        if len(tile_number_possibilities) == 0 or len(possible_sets) == 0:
            return []
        hold = []
        combine = list(itertools.product(possible_sets,tile_number_possibilities))
        for a,b in combine:
            status = True
            for v in a:
                if v not in b:
                    status = False
                    break
            if status:
                hold.append(a)
        return set(hold)

    @staticmethod
    def product(t):
        v = t[0]
        for x in t[1:]:
            v *= x
        return v
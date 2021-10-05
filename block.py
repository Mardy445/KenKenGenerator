import random
import itertools
from collections import Counter
import copy

"""
This file contains the Block object which represents each block of the KenKen board.
It generates blocks by attempting to add a neighbouring position to it at each iteration
"""


class Block:
    positions = []
    sign = None
    value = 0
    numbers = []

    p1_range = 1
    p2_range = 1
    p1_absolutes = []
    p2_absolutes = []

    complete = False

    def __init__(self, init, init_number, sz):
        self.numbers = []
        self.positions = []
        self.positions.append(init)
        self.top_left_position = init
        self.numbers.append(init_number)
        self.sz = sz
        self.p1_absolutes = []
        self.p2_absolutes = []

    def get_top_left_most_position(self):
        hold_positions = copy.copy(self.positions)
        hold_positions.sort(key=lambda y: y[0])
        highest_p1 = hold_positions[0][0]
        hold_positions = [p for p in hold_positions if p[0] == highest_p1]
        hold_positions.sort(key=lambda y: y[1])
        return hold_positions[0]


    """
    Appends a new position to the block
    """

    def add_new_tile(self, pos, number):
        self.positions.append(pos)
        self.p1_range = len({p[0] for p in self.positions})
        self.p2_range = len({p[1] for p in self.positions})
        self.numbers.append(number)
        self.top_left_position = self.get_top_left_most_position()

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
        v = v2 / v1 if v2 > v1 else v1 / v2

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

    def calculate_all_possible_sets(self, grid, reserved_values_p1, reserved_values_p2):
        if self.sign is None:
            return [[self.value]], [(self.value)]

        n = len(self.positions)
        tile_number_possibilities = []
        possible_sets = []

        # Firstly determines what values are possible based on surrounding blocks and tiles
        for pos in self.positions:
            if grid[pos[0]][pos[1]] != 0:
                hold = [grid[pos[0]][pos[1]]]
            else:
                hold = [x + 1 for x in range(self.sz)]
                for i in range(self.sz):
                    if i != pos[1] and grid[pos[0]][i] in hold:
                        hold.remove(grid[pos[0]][i])
                    if (pos[0],i) not in self.positions:
                        for rv in reserved_values_p1[pos[0]][i]:
                            if rv in hold:
                                hold.remove(rv)
                    if i != pos[0] and grid[i][pos[1]] in hold:
                        hold.remove(grid[i][pos[1]])
                    if (i,pos[1]) not in self.positions:
                        for rv in reserved_values_p2[i][pos[1]]:
                            if rv in hold:
                                hold.remove(rv)
            tile_number_possibilities.append(hold)
        # Generates a list of all possible permutation of numbers given the possible numbers for each tile
        tile_number_possibilities_sets = list(itertools.product(*tile_number_possibilities))

        # Next up calculates the possible permutations of N numbers given the sign and value
        # If +, determines all possible permutations given all numbers less than the value
        # If there are more than 2 tiles in this block, remove more values from the end of the list
        # (since each tile must at least equal 1). Then only keep permutations that sum to value
        if self.sign == "+":
            possible_numbers = [x + 1 for x in range(self.sz) if x + 1 < (self.value - (n - 2))]
            possible_sets = list(itertools.combinations_with_replacement(possible_numbers, n))
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
            possible_sets = [t for t in possible_sets if
                             max(t) / min(t) == self.value and (max(t) / min(t)) - int(max(t) / min(t)) == 0]
        # If *, determine all factors of value in the list of numbers from 1->sz
        # Determine all permutations of these numbers, and keep any where the product is value
        if self.sign == "*":
            possible_numbers = [x + 1 for x in range(self.sz) if self.value % (x + 1) == 0]
            possible_sets = list(itertools.combinations_with_replacement(possible_numbers, n))
            possible_sets = [t for t in possible_sets if self.product(t) == self.value]

        # With these 2 lists of permutations, find the intersection (IE the list of values that are common to both)
        same = self.intersection_of_tiles_and_possible_sets(possible_sets, tile_number_possibilities_sets)
        same = [t for t in same if self.are_values_valid_relative_to_each_other(t)]

        return tile_number_possibilities, same

    def get_tile_unique_boolean_values(self, grid, reserved_values_p1, reserved_values_p2, solving=False, multiple_paths=False):
        if len(self.positions) == 1:
            return [self.value], [], []

        tile_number_possibilities, same = self.calculate_all_possible_sets(grid, reserved_values_p1, reserved_values_p2)
        contains_actual_value = self.does_same_contain_actual_value(same)

        if (len(same) == 1 and (contains_actual_value or solving)) or multiple_paths:
            return list(same[0]), [], []
        elif len(same) > 1 and (contains_actual_value or solving):
            len_check = [
                len(tile_number_possibilities[i]) == 1 and grid[self.positions[i][0]][self.positions[i][1]] == 0 for i
                in range(len(tile_number_possibilities))]
            hold_p1_absolutes = [i + 1 for i in range(self.sz)]
            hold_p2_absolutes = [i + 1 for i in range(self.sz)]
            counts = [Counter(x) for x in same]
            for i in range(self.sz):
                b1 = b2 = True
                for c in counts:
                    if not b1 and not b2:
                        break
                    if b1 and (not c[i + 1] == self.p1_range or i + 1 in self.p1_absolutes):
                        hold_p1_absolutes.remove(i + 1)
                        b1 = False
                    if b2 and (not c[i + 1] == self.p2_range or i + 1 in self.p2_absolutes):
                        hold_p2_absolutes.remove(i + 1)
                        b2 = False
            return [tile_number_possibilities[i][0] if len_check[i] else 0 for i in range(len(len_check))], hold_p1_absolutes, hold_p2_absolutes
        else:
            return [0] * len(self.positions), [], []

    def are_values_valid_relative_to_each_other(self, values):
        index_pairs = set(itertools.combinations([x for x in range(len(self.positions))], 2))
        for i1, i2 in index_pairs:
            if self.positions[i1][0] == self.positions[i2][0] or self.positions[i1][1] == self.positions[i2][1]:
                if values[i1] == values[i2]:
                    return False
        return True

    def does_same_contain_actual_value(self, same):
        return any([t == tuple(self.numbers) for t in same])

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
        combine = list(itertools.product(tile_number_possibilities, possible_sets))
        for a, b in combine:
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

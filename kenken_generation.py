import random
import copy
import sys

"""
This file contains the primary code for generating a KenKen grid

Using backtracking, it determines if, given the number grid and the block segments, whether a sign can be assigned to 
each block such that a solution exists where there is a non-ambiguous way of completing the grid from start to finish
"""


class KenKenGenerator:
    stack = []

    def __init__(self, sz, grid, blocks):
        self.grid = grid
        self.sz = sz
        init_grid = []
        hold = [0] * sz
        for i in range(sz):
            init_grid.append(hold.copy())
        self.stack.append(KenKenGeneratorBacktrackingNode(init_grid, blocks, []))

    """
    Uses backtracking algorithm techniques to randomly generate a valid grid
    """

    def begin_generation(self):
        fail_count = 0
        while len(self.stack) > 0:
            # Peeks at the node on top of the stack
            node = self.stack[len(self.stack) - 1]

            # If no blocks remain to be processed in the node, it has successfully assigned signs to each block
            if len(node.remaining_blocks) == 0:
                return node

            # Requests the block to return the next node if possible to put on the stack
            new_node = node.get_next_valid_child_node(self.grid)
            if new_node is not None:
                self.stack.append(new_node)
            elif fail_count == 20:
                return None
            else:
                fail_count += 1
                self.stack.pop()

        # There may be no way of assigning signs to the blocks such that an unambiguous solution exists
        # In which case, return None
        return None

    """
    This method is used after generation to return the information needed to display the KenKen grid in Tkinter
    """

    def convert_blocks_to_border_maps_and_sign_values(self, blocks):
        border_maps = []
        sign_values = []

        hold = [""] * self.sz
        for i in range(self.sz):
            border_maps.append(hold.copy())
            sign_values.append(hold.copy())

        for i, block in enumerate(blocks):
            block.positions.sort(key=lambda y: y[0])
            sign_values[block.positions[0][0]][block.positions[0][1]] = (
                                                                            block.sign if block.sign is not None else "") + str(
                int(block.value))

            for pos in block.positions:
                if (pos[0], pos[1] + 1) not in block.positions and pos[1] + 1 < self.sz:
                    border_maps[pos[0]][pos[1]] += "e"
                if (pos[0] + 1, pos[1]) not in block.positions and pos[0] + 1 < self.sz:
                    border_maps[pos[0]][pos[1]] += "s"

        return border_maps, sign_values


"""
This class represents a single node used in this backtracking algorithm
"""


class KenKenGeneratorBacktrackingNode:
    def __init__(self, current_grid, remaining_blocks, complete_blocks):
        self.current_grid = current_grid
        self.remaining_blocks = remaining_blocks
        self.complete_blocks = complete_blocks
        self.signs = ["+", "-", "*", "/"]
        self.i = 0

        #random.shuffle(self.remaining_blocks)
        random.shuffle(self.signs)

    """
    Returns the next valid node such that a non-ambiguous step exists from this node to the returned node
    """
    def get_next_valid_child_node(self, number_grid):
        if self.i == len(self.remaining_blocks):
            return None

        block = copy.copy(self.remaining_blocks[self.i])

        #print(self.i,len(self.remaining_blocks))

        if len(block.positions) == 1:
            block.set_value(number_grid[block.positions[0][0]][block.positions[0][1]])
            self.signs = []
            return self.generate_new_node(block, number_grid,[True])
        else:
            while len(self.signs) > 0:
                sign = self.signs.pop()
                if sign == "+":
                    block.calculate_plus(number_grid)
                elif sign == "-":
                    block.calculate_minus(number_grid)
                elif sign == "*":
                    block.calculate_multiply(number_grid)
                elif sign == "/":
                    block.calculate_divide(number_grid)
                if block.sign is not None:
                    unique_bool_array = block.get_tile_unique_boolean_values(self.current_grid)
                    if any(unique_bool_array):
                        return self.generate_new_node(block, number_grid, unique_bool_array)
                    else:
                        block.reset_value_and_sign()

        self.signs = ["+", "-", "*", "/"]
        random.shuffle(self.signs)
        self.i += 1
        return self.get_next_valid_child_node(number_grid)

    def generate_new_node(self, block, number_grid, unique_bool_array):
        hold_grid = copy.deepcopy(self.current_grid)
        hold_remaining_blocks = copy.copy(self.remaining_blocks)
        hold_complete_blocks = copy.deepcopy(self.complete_blocks)
        for i,pos in enumerate(block.positions):
            if unique_bool_array[i]:
                hold_grid[pos[0]][pos[1]] = number_grid[pos[0]][pos[1]]

        if all(unique_bool_array):
            del hold_remaining_blocks[self.i]
            hold_complete_blocks.append(block)
        return KenKenGeneratorBacktrackingNode(hold_grid, hold_remaining_blocks, hold_complete_blocks)

    # Returns True if for a given block, there is only 1 possible input
    def is_block_solution_unique(self, block):
        return all(block.calculate_all_possible_sets(self.current_grid))

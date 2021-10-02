import copy
import random
from block import Block

"""
This file contains the code to randomly segment a sz*sz square into a number of Blocks 
"""


class KenKenGenerationBlockByBlock:
    current_attempts = 0

    def __init__(self, sz, number_grid):
        self.sz = sz
        self.number_grid = number_grid

        init_grid = []
        hold = [0] * sz
        for i in range(sz):
            init_grid.append(hold.copy())

        init_reserved_values_p1 = []
        init_reserved_values_p2 = []
        hold = []
        for i in range(sz):
            hold.append([])
        for i in range(sz):
            init_reserved_values_p1.append(copy.deepcopy(hold))
            init_reserved_values_p2.append(copy.deepcopy(hold))

        init_available_positions = []
        for x in range(self.sz):
            for y in range(self.sz):
                init_available_positions.append((x, y))
        random.shuffle(init_available_positions)

        self.current_grid = init_grid
        self.reserved_values_grid_p1 = init_reserved_values_p1
        self.reserved_values_grid_p2 = init_reserved_values_p2
        self.available_positions = init_available_positions
        self.blocks = []

    def generate_kenken_grid(self):
        while len(self.available_positions) > 0:
            block = self.generate_random_block(self.available_positions)
            if (len(block.positions) == 1):
                block.set_value(self.number_grid[block.positions[0][0]][block.positions[0][1]])
                self.generate_new_node(block,[True],[],[])
                print(len(self.available_positions))
                continue

            signs = ["+", "-", "*", "/"]
            random.shuffle(signs)
            for sign in signs:
                if sign == "+":
                    block.calculate_plus(self.number_grid)
                elif sign == "-":
                    block.calculate_minus(self.number_grid)
                elif sign == "*":
                    block.calculate_multiply(self.number_grid)
                elif sign == "/":
                    block.calculate_divide(self.number_grid)
                if block.sign is not None:
                    unique_bool_array, hold_p1_absolutes, hold_p2_absolutes = block.get_tile_unique_boolean_values(
                        self.current_grid, self.reserved_values_grid_p1, self.reserved_values_grid_p2)
                    if any(unique_bool_array) or len(hold_p1_absolutes) > 0 or len(hold_p2_absolutes) > 0:
                        self.generate_new_node(block, unique_bool_array, hold_p1_absolutes, hold_p2_absolutes)
                        print(len(self.available_positions))
                        self.current_attempts = 0
                        break
                    else:
                        block.reset_value_and_sign()
            self.current_attempts += 1

    def generate_random_block(self, available_positions):
        block_init_pos = available_positions[random.randint(0, len(available_positions) - 1)]
        block = Block(block_init_pos, self.number_grid[block_init_pos[0]][block_init_pos[1]],self.sz)
        if self.current_attempts == 20:
            self.current_attempts = 0
            return block

        r = 0
        f = 1
        while r < f and len(block.positions) < 5:
            pos = block.get_possible_next_position(available_positions)
            # If no possible neighbours, end generation for this block
            if pos is not None:
                block.add_new_tile(pos, self.number_grid[pos[0]][pos[1]])
                r = random.uniform(0, 1)
                f = (0.5)
            else:
                break
        return block

    def generate_new_node(self, block, unique_bool_array, hold_p1_absolutes, hold_p2_absolutes):
        self.update_values_given_block(block,unique_bool_array,hold_p1_absolutes,hold_p2_absolutes)
        for pos in block.positions:
            self.available_positions.remove(pos)

        for hold_block in self.blocks:
            if hold_block.complete:
                continue
            u, p1_a, p2_a = hold_block.get_tile_unique_boolean_values(self.current_grid, self.reserved_values_grid_p1, self.reserved_values_grid_p2)
            self.update_values_given_block(hold_block,u,p1_a,p2_a)

        self.blocks.append(block)

    def update_values_given_block(self,block, unique_bool_array, hold_p1_absolutes, hold_p2_absolutes):
        if all(unique_bool_array):
            block.complete = True
        for i, pos in enumerate(block.positions):
            if unique_bool_array[i]:
                self.current_grid[pos[0]][pos[1]] = self.number_grid[pos[0]][pos[1]]
            self.reserved_values_grid_p1[pos[0]][pos[1]].extend(hold_p1_absolutes)
            self.reserved_values_grid_p2[pos[0]][pos[1]].extend(hold_p2_absolutes)
            block.p1_absolutes.extend(hold_p1_absolutes)
            block.p2_absolutes.extend(hold_p2_absolutes)


    def convert_blocks_to_border_maps_and_sign_values(self):
        border_maps = []
        sign_values = []

        hold = [""] * self.sz
        for i in range(self.sz):
            border_maps.append(hold.copy())
            sign_values.append(hold.copy())

        for i, block in enumerate(self.blocks):
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

# import copy
# import random
# from block import Block
#
# """
# This file contains the code to randomly segment a sz*sz square into a number of Blocks
# """
#
#
# class KenKenGenerationBlockByBlock:
#     stack = []
#
#     def __init__(self, sz, number_grid):
#         self.sz = sz
#         self.number_grid = number_grid
#
#         init_grid = []
#         hold = [0] * sz
#         for i in range(sz):
#             init_grid.append(hold.copy())
#
#         init_reserved_values = []
#         hold = []
#         for i in range(sz):
#             hold.append([])
#         for i in range(sz):
#             init_reserved_values.append(copy.deepcopy(hold))
#
#         init_available_positions = []
#         for x in range(self.sz):
#             for y in range(self.sz):
#                 init_available_positions.append((x, y))
#         random.shuffle(init_available_positions)
#
#         self.stack.append(BacktrackingBlock(init_grid, init_reserved_values,init_available_positions,[],0))
#
#     def generate_kenken_grid(self):
#         while len(self.stack) > 0:
#             node = self.stack[len(self.stack)-1]
#
#             if len(node.available_positions) == 0:
#                 return node
#
#             block = self.generate_random_block(node.available_positions)
#
#             signs = ["+", "-", "*", "/"]
#             random.shuffle(signs)
#             for sign in signs:
#                 if sign == "+":
#                     block.calculate_plus(self.number_grid)
#                 elif sign == "-":
#                     block.calculate_minus(self.number_grid)
#                 elif sign == "*":
#                     block.calculate_multiply(self.number_grid)
#                 elif sign == "/":
#                     block.calculate_divide(self.number_grid)
#                 if block.sign is not None:
#                     unique_bool_array,hold_p1_absolutes,hold_p2_absolutes = block.get_tile_unique_boolean_values(node.current_grid, node.reserved_values_grid)
#                     if any(unique_bool_array) or len(hold_p1_absolutes) > 0 or len(hold_p2_absolutes) > 0:
#                         self.stack.append(self.generate_new_node(node, block, unique_bool_array, hold_p1_absolutes, hold_p2_absolutes))
#                         print(len(self.stack[len(self.stack)-1].available_positions))
#                         break
#                     else:
#                         block.reset_value_and_sign()
#             if block.sign is None:
#                 node.number_of_attempts += 1
#
#
#
#     def generate_random_block(self, available_positions):
#         block_init_pos = available_positions[random.randint(0,len(available_positions)-1)]
#         block = Block(block_init_pos, self.sz)
#
#         r = random.uniform(0, 1)
#         f = (1 / (len(block.positions) + 0.01))
#         while r < f and len(block.positions) < self.sz:
#             pos = block.get_possible_next_position(available_positions)
#             # If no possible neighbours, end generation for this block
#             if pos is not None:
#                 block.add_new_tile(pos)
#                 r = random.uniform(0, 1)
#                 f = (1 / (len(block.positions) + 0.01))
#             else:
#                 break
#         return block
#
#     def generate_new_node(self, node, block, unique_bool_array, hold_p1_absolutes, hold_p2_absolutes):
#         hold_grid = copy.deepcopy(node.current_grid)
#         hold_available_positions = copy.copy(node.available_positions)
#         hold_reserved_values = copy.deepcopy(node.reserved_values_grid)
#         hold_blocks = copy.deepcopy(node.blocks)
#
#         for i, pos in enumerate(block.positions):
#             if unique_bool_array[i]:
#                 hold_grid[pos[0]][pos[1]] = self.number_grid[pos[0]][pos[1]]
#             hold_reserved_values[pos[0]][pos[1]].extend(hold_p1_absolutes)
#             hold_reserved_values[pos[0]][pos[1]].extend(hold_p2_absolutes)
#             block.p1_absolutes.extend(hold_p1_absolutes)
#             block.p2_absolutes.extend(hold_p2_absolutes)
#             hold_available_positions.remove(pos)
#
#         hold_blocks.append(block)
#
#         return BacktrackingBlock(hold_grid,hold_reserved_values,hold_available_positions,hold_blocks,node.depth+1)
#
#     def convert_blocks_to_border_maps_and_sign_values(self, blocks):
#         border_maps = []
#         sign_values = []
#
#         hold = [""] * self.sz
#         for i in range(self.sz):
#             border_maps.append(hold.copy())
#             sign_values.append(hold.copy())
#
#         for i, block in enumerate(blocks):
#             block.positions.sort(key=lambda y: y[0])
#             sign_values[block.positions[0][0]][block.positions[0][1]] = (
#                                                                             block.sign if block.sign is not None else "") + str(
#                 int(block.value))
#
#             for pos in block.positions:
#                 if (pos[0], pos[1] + 1) not in block.positions and pos[1] + 1 < self.sz:
#                     border_maps[pos[0]][pos[1]] += "e"
#                 if (pos[0] + 1, pos[1]) not in block.positions and pos[0] + 1 < self.sz:
#                     border_maps[pos[0]][pos[1]] += "s"
#
#         return border_maps, sign_values
#
#
# class BacktrackingBlock:
#     def __init__(self, current_grid, reserved_values_grid, available_positions, blocks, depth):
#         self.current_grid = current_grid
#         self.reserved_values_grid = reserved_values_grid
#         self.available_positions = available_positions
#         self.blocks = blocks
#         self.number_of_attempts = 0
#         self.depth = depth
#         return

from generate_number_grid import KenKenGrid
from custom_tile import TileFrame
from kenken_generation import KenKenGenerationBlockByBlock, get_empty_grid_of_lists, get_empty_grid_of_zeroes
from randomly_generate_blocks import RandomGridSegmentation
import tkinter as tk
import copy
import random

DELAY_LOWER_BOUND = 50
DELAY_UPPER_BOUND = 300

RANDOMLY_GENERATE_GRID = False


def is_zero_in_grid(grid):
    for row in grid:
        if 0 in row:
            return True
    return False


class TkinterGrid:
    shift_mode = False

    def __init__(self, grid, root, sz):
        self.grid = grid
        self.sz = sz
        self.current = (0, 0)
        self.delay = 300
        root.bind('f', self.change_delay)
        grid[0][0].focus()
        self.bind_events()

    def bind_events(self):
        root.bind('<Left>', self.left)
        root.bind('<Right>', self.right)
        root.bind('<Up>', self.up)
        root.bind('<Down>', self.down)
        root.bind('<BackSpace>', self.back)
        root.bind('<Shift-KeyPress-BackSpace>', self.back_shift)
        root.bind('<space>', self.solve_game)
        for i in range(6):
            root.bind(f"<KeyPress-{str(i + 1)}>", self.number_handler)
        root.bind(f"<Shift-Key>", self.number_handler_shift)

    def unbind_events(self):
        root.unbind('<Left>')
        root.unbind('<Right>')
        root.unbind('<Up>')
        root.unbind('<Down>')
        root.unbind('<BackSpace>')
        root.unbind('<Shift-KeyPress-BackSpace>')
        root.unbind('<space>')
        for i in range(6):
            root.unbind(f"<KeyPress-{str(i + 1)}>")
        root.unbind(f"<Shift-Key>")

    def solve_game(self, event):
        self.reset_all()
        current_grid = get_empty_grid_of_zeroes(self.sz)
        reserved_values_grid_p1 = get_empty_grid_of_lists(self.sz)
        reserved_values_grid_p2 = copy.deepcopy(reserved_values_grid_p1)
        blocks = main_generator.blocks
        random.shuffle(blocks)
        text_list.delete(0, 'end')
        for block in blocks:
            block.complete = False
            block.p1_absolutes = []
            block.p2_absolutes = []
        self.unbind_events()
        root.after(0, self.take_one_solve_game_step, current_grid, reserved_values_grid_p1, reserved_values_grid_p2,
                   blocks)

    def take_one_solve_game_step(self, current_grid, reserved_values_grid_p1, reserved_values_grid_p2, blocks, index=0,
                                 single_step_taken=False, multiple_paths_exist=False):
        block = blocks[index]
        is_block_init_complete = block.complete
        if not is_block_init_complete:
            self.unfocus_all()
            unique_value_list, hold_p1_absolutes, hold_p2_absolutes = block.get_block_information(
                current_grid, reserved_values_grid_p1, reserved_values_grid_p2, True, multiple_paths_exist)
            if all(unique_value_list):
                block.complete = True
            if any(unique_value_list) or len(hold_p1_absolutes) > 0 or len(hold_p2_absolutes) > 0:
                single_step_taken = True
                multiple_paths_exist = False
            for i, pos in enumerate(block.positions):
                self.grid[pos[1]][pos[0]].focus()
                v = unique_value_list[i]
                if v:
                    current_grid[pos[0]][pos[1]] = v
                    self.grid[pos[1]][pos[0]].set_number(v)
                reserved_values_grid_p1[pos[0]][pos[1]].extend(hold_p1_absolutes)
                reserved_values_grid_p2[pos[0]][pos[1]].extend(hold_p2_absolutes)
                block.p1_absolutes.extend(hold_p1_absolutes)
                block.p2_absolutes.extend(hold_p2_absolutes)
                self.grid[pos[1]][pos[0]].add_numbers_to_possibilities_list(reserved_values_grid_p1[pos[0]][pos[1]])
                self.grid[pos[1]][pos[0]].add_numbers_to_possibilities_list(reserved_values_grid_p2[pos[0]][pos[1]])
            self.log(block, unique_value_list, hold_p1_absolutes, hold_p2_absolutes)
        new_index = (index + 1) % len(blocks)
        if new_index <= index:
            if not single_step_taken:
                text_list.insert("end", f"Multiple equally viable paths exist. Take first one")
                multiple_paths_exist = True
            single_step_taken = False

        if is_zero_in_grid(current_grid):
            root.after(self.delay if not is_block_init_complete else 0, self.take_one_solve_game_step, current_grid,
                       reserved_values_grid_p1,
                       reserved_values_grid_p2, blocks, new_index, single_step_taken, multiple_paths_exist)
        else:
            self.unfocus_all()
            self.bind_events()

    def log(self, block, values, reserved_values_p1, reserved_values_p2):
        reserved_values_p1.extend(reserved_values_p2)
        reserved_values = set(reserved_values_p1)
        block = f"Block {'' if block.sign is None else block.sign}{block.value} {block.top_left_position}"
        if any(values):
            text_list.insert("end", f"{block} contains {[v for v in values if not v == 0]} in known tiles")
        if len(reserved_values) > 0:
            text_list.insert("end", f"{block} contains {reserved_values} in unknown tiles")
        if not any(values) and len(reserved_values) == 0:
            text_list.insert("end", f"No useful information from {block} as of yet")

    def change_delay(self, event):
        self.delay = DELAY_LOWER_BOUND if self.delay == DELAY_UPPER_BOUND else DELAY_UPPER_BOUND

    def left(self, event):
        self.move_current((-1, 0))

    def right(self, event):
        self.move_current((1, 0))

    def up(self, event):
        self.move_current((0, -1))

    def down(self, event):
        self.move_current((0, 1))

    def back(self, event):
        grid[self.current[0]][self.current[1]].set_number("")

    def back_shift(self, event):
        grid[self.current[0]][self.current[1]].pop_from_possibilities_list()

    def number_handler(self, event):
        grid[self.current[0]][self.current[1]].set_number(event.char)

    def number_handler_shift(self, event):
        keys = ['!', '"', '??', '$', '%', '^']
        if event.char not in keys:
            return
        number = keys.index(event.char) + 1
        grid[self.current[0]][self.current[1]].add_number_to_possibilities_list(number)

    def move_current(self, next_pos):
        grid[self.current[0]][self.current[1]].unfocus()
        self.current = ((self.current[0] + next_pos[0]) % self.sz, (self.current[1] + next_pos[1]) % self.sz)
        grid[self.current[0]][self.current[1]].focus()

    def reset_all(self):
        for c in range(self.sz):
            for r in range(self.sz):
                grid[r][c].reset()

    def unfocus_all(self):
        for c in range(self.sz):
            for r in range(self.sz):
                grid[r][c].unfocus()


"""
Returns the information needed by the GUI to show the grid.
border_maps: A grid where each element describes what borders it needs
signs_values: A grid where each element represents what to put for the top left corner label. 
            Either (sign + value) if top left corner of block or "" otherwise.
"""


def convert_blocks_to_border_maps_and_sign_values(blocks, sz):
    border_maps = []
    sign_values = []

    hold = [""] * sz
    for i in range(sz):
        border_maps.append(hold.copy())
        sign_values.append(hold.copy())

    for i, block in enumerate(blocks):
        sign_values[block.top_left_position[0]][block.top_left_position[1]] = (
                                                                                  block.sign if block.sign is not None else "") + str(
            int(block.value))

        for pos in block.positions:
            if (pos[0], pos[1] + 1) not in block.positions and pos[1] + 1 < sz:
                border_maps[pos[0]][pos[1]] += "e"
            if (pos[0] + 1, pos[1]) not in block.positions and pos[0] + 1 < sz:
                border_maps[pos[0]][pos[1]] += "s"

    return border_maps, sign_values


if __name__ == '__main__':
    size = 6

    # Generates a valid grid of numbers
    number_grid_generator = KenKenGrid(size)
    n_grid = None
    while n_grid is None:
        n_grid = number_grid_generator.generate_random_grid()

    # Uses this grid of numbers to generate the kenken grid
    if not RANDOMLY_GENERATE_GRID:
        main_generator = KenKenGenerationBlockByBlock(size, n_grid)
        main_generator.generate_kenken_grid()
    else:
        main_generator = RandomGridSegmentation(size, n_grid)
        main_generator.randomly_segment_grid()

    # Gets the information needed by the GUI
    border_code, sign_values = convert_blocks_to_border_maps_and_sign_values(main_generator.blocks,size)

    # Creates the GUI
    grid = []
    root = tk.Tk()
    right_panel = tk.Frame(root)
    right_panel.grid(row=0, column=size, rowspan=size)
    text_list = tk.Listbox(right_panel, height=3 * size, width=45)
    text_list.grid(row=0)
    for c in range(size):
        hold = []
        for r in range(size):
            frame = TileFrame(root, border_code[r][c], sign_values[r][c], "")
            frame.grid(row=r, column=c)
            hold.append(frame)
        grid.append(hold)

    # Creates a TkinterGrid object, which creates key bindings to modify the grid
    TkinterGrid(grid, root, size)
    root.mainloop()

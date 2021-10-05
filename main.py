from generate_number_grid import KenKenGrid
from custom_tile import TileFrame
from kenken_generation_by_blocks import KenKenGenerationBlockByBlock, get_empty_grid_of_lists, get_empty_grid_of_zeroes
import tkinter as tk
import copy
import random


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
        for block in blocks:
            block.complete = False
            block.p1_absolutes = []
            block.p2_absolutes = []
        self.unbind_events()
        root.after(100, self.take_one_solve_game_step, current_grid, reserved_values_grid_p1, reserved_values_grid_p2,
                   blocks)

    def take_one_solve_game_step(self, current_grid, reserved_values_grid_p1, reserved_values_grid_p2, blocks, index=0, single_step_taken=False, multiple_paths_exist=False):
        block = blocks[index]
        is_block_init_complete = block.complete
        if not is_block_init_complete:
            self.unfocus_all()
            unique_value_list, hold_p1_absolutes, hold_p2_absolutes = block.get_tile_unique_boolean_values(
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
        new_index = (index + 1) % len(blocks)
        if new_index <= index:
            if not single_step_taken:
                multiple_paths_exist = True
            single_step_taken = False


        if is_zero_in_grid(current_grid):
            root.after(100 if not is_block_init_complete else 0, self.take_one_solve_game_step, current_grid, reserved_values_grid_p1,
                       reserved_values_grid_p2, blocks, new_index, single_step_taken, multiple_paths_exist)
        else:
            self.unfocus_all()
            self.bind_events()

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
        keys = ['!', '"', '£', '$', '%', '^']
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


if __name__ == '__main__':

    size = 6
    #random.seed(16)
    number_grid_generator = KenKenGrid(size)
    number_grid_generator.generate_random_grid()
    n_grid = number_grid_generator.grid

    main_generator = KenKenGenerationBlockByBlock(size, n_grid)
    main_generator.generate_kenken_grid()
    border_code, sign_values = main_generator.convert_blocks_to_border_maps_and_sign_values()

    grid = []
    root = tk.Tk()

    # root.rowconfigure(tuple(range(size)), weight=1)
    # root.columnconfigure(tuple(range(size)), weight=1)

    for c in range(size):
        hold = []
        for r in range(size):
            frame = TileFrame(root, border_code[r][c], sign_values[r][c], "")
            frame.position_in_grid(r, c)
            hold.append(frame)
        grid.append(hold)

    TkinterGrid(grid, root, size)
    root.mainloop()

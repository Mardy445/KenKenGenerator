from generate_number_grid import KenKenGrid
from custom_tile import TileFrame
from kenken_generation_by_blocks import KenKenGenerationBlockByBlock
import tkinter as tk
import random


class TkinterGrid:
    def __init__(self, grid, root, sz):
        self.grid = grid
        self.sz = sz
        self.current = (0, 0)
        root.bind('<Left>', self.left)
        root.bind('<Right>', self.right)
        root.bind('<Up>', self.up)
        root.bind('<Down>', self.down)
        root.bind('<BackSpace>', self.back)
        for i in range(6):
            root.bind(str(i+1), self.number_handler)

    def left(self,event):
        self.move_current((-1,0))

    def right(self,event):
        self.move_current((1,0))

    def up(self,event):
        self.move_current((0,-1))

    def down(self,event):
        self.move_current((0,1))

    def back(self,event):
        grid[self.current[0]][self.current[1]].set_number("")

    def number_handler(self,event):
        grid[self.current[0]][self.current[1]].set_number(event.char)

    def move_current(self, next_pos):
        grid[self.current[0]][self.current[1]].unfocus()
        self.current = ((self.current[0] + next_pos[0]) % self.sz, (self.current[1] + next_pos[1]) % self.sz)
        grid[self.current[0]][self.current[1]].focus()


if __name__ == '__main__':

    size = 6
    #random.seed(15)
    number_grid_generator = KenKenGrid(size)
    number_grid_generator.generate_random_grid()
    n_grid = number_grid_generator.grid

    main_generator = KenKenGenerationBlockByBlock(size,n_grid)
    main_generator.generate_kenken_grid()
    border_code, sign_values = main_generator.convert_blocks_to_border_maps_and_sign_values()

    grid = []

    root = tk.Tk()
    for c in range(size):
        hold = []
        for r in range(size):
            frame = TileFrame(root, border_code[r][c], sign_values[r][c], "")
            frame.position_in_grid(r, c)
            hold.append(frame)
        grid.append(hold)

    TkinterGrid(grid,root,size)
    root.mainloop()


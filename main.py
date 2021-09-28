from generate_number_grid import KenKenGrid
from generate_segemented_grid_map import RandomGridSegmentation
from custom_tile import TileFrame
from kenken_generation import KenKenGenerator
import tkinter as tk
import random

if __name__ == '__main__':
    size = 8
    #random.seed(14)
    number_grid_generator = KenKenGrid(size)
    number_grid_generator.generate_random_grid()
    n_grid = number_grid_generator.grid

    grid_map_generator = RandomGridSegmentation(size)

    main_generator = None
    usable_node = None
    while usable_node is None:
        grid_map_generator.segment_grid()
        main_generator = KenKenGenerator(size, n_grid, grid_map_generator.blocks)
        usable_node = main_generator.begin_generation()

    border_code, sign_values = main_generator.convert_blocks_to_border_maps_and_sign_values(usable_node.complete_blocks)

    root = tk.Tk()

    for c in range(size):
        for r in range(size):
            frame = TileFrame(root, border_code[r][c], sign_values[r][c], n_grid[r][c])
            frame.position_in_grid(r, c)
    root.mainloop()

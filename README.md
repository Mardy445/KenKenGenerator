# KenKen Generator and Solver

##### What is KenKen?
KenKen is a logic and arithmetic based game that shares many traits with sudoku.
You need to fill out an NxN grid with numbers from 1-N such that every row and column contains only 1 of each possible number.
The grid is also segmented where each segment (referred to as blocks throughout my code)
has an arithmetic sign and a value. The contents of each segment must equal the value when put through the function represented by the sign.
 For example, a block with the plus sign and a value of 7 must have all its tiles sum up to 7.
 
##### Motivation For Project
I heard that a good project for any resume was a Sudoku generation program. I figured I would try to be a bit more interesting
with a KenKen generator.

##### Project Dependencies
This project was developed using only the python standard library with Python 3.7.

##### How to Use
Controls:
* Arrow Keys: Move the focus between tiles
* Numbers: Insert number into Tile
* Shift-Numbers: Insert Number into bottom left list for note purposes
* Backspace: Remove number from tile
* Shift-Backspace: Remove number from bottom left list
* Space: Begin auto solving the generated game
* F: Swap between slow solving and fast solving speeds

The list on the right will display the information gathered during each step of solving.
If you wish to mess around with grid sizes greater than or less than 6, you can alter the size parameter
in the main file. There is an upper limit which is dependant on your devices memory. The number of possible combinations per block
is at most (SIZE!). I would not recommend going over a size of 15.

##### How It Works
Below is a very simply description of how games are generated such that a solution is certainly achievable
* Generate a grid of numbers using backtracking such that each row and column contains only 1 of each possible number
* While there are tiles on the grid not in a block, iterative generate new blocks
* If a newly generated block provides no useful information, dont add the block
* Otherwise, add the block
* If a certain number of failed blocks are generated since the previous successful block, then generate a block with only 1 tile (since this will always provide information)

Taking these steps ensures that a solution will exist that can be achieved via logical steps.

This program also contains the means to simply randomly generate a KenKen grid with no regards to if it is solvable without backtracking. If you would like to test this functionality out, change the global variable in main RANDOMLY_GENERATE_GRID from False to True. It generates more natural looking games, but may have paths to take where you get "stuck" and need to backtrack,
unlike the method described above. 

##### Improvements I would like to Make
* The main improvement I would like to make is to have the program generate more natural looking games. To do this, one modifications to
be made is that less "single tile blocks" are generated. Encouraging the generator to produce more interesting shaped blocks (such as squares) would also be good.
* General improvements to the GUI





# conways_game_of_life
This is a repo for the practical session in software development training, intended for the hypso sw group.
The Presentation and a compiled docker image can be found here(TBD). The tasks are intended to be completed in python.

## The Rules of the Game

Conway's Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves.

The rules of the game:
* Any cell can be either alive or dead
* Any live cell with fewer than two live neighbours dies, as if by underpopulation
* Any live cell with two or three live neighbours lives on to the next generation
* Any live cell with more than three live neighbours dies, as if by overpopulation
* Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction

To learn more about the game please visit these relevant links:
* https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
* Gardner, Martin (October 1970). "Mathematical Games - The Fantastic Combinations of John Conway's New Solitaire Game 'Life'". Scientific American (223): 120–123. doi:10.1038/scientificamerican1070-120.
*

## Tasks
The following tasks is part of the practical session
* Implement the rules of the game
* Make a 40x40 grid of cells, randomly initialized
* Simulate 100 iterations
* Decide what to do on the edge or border of the grid
* Utilze the following tools during development
  * Docker
  * Pylint
  * autopep8
  * Each other
  * Github Flow
* Test your code using pytest.

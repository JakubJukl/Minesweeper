# Minesweeper
Given you have python installed:
Run `pip3 install -r requirements.txt` to install pygame  
Run `python runner.py`in this directory to run the game  

## Config
**WINDOW_WIDTH** - window width in pixels  
**WINDOW_HEIGHT** - windows height in pixels  
**HEIGHT_TILES** - game board height in number of cells  
**WIDTH_TILES** - game board width in number of cells  
**MINE_TILES** - number of cells with mines  
**AI_KNOWS_NUMBER_OF_MINES** - 1 if AI player should know how many mines there are in the game board  
**AI_SEARCH_ASAP** - 1 if AI player should calculate mines and safe moves as soon as possible  

## How it works
AI player keep knowledge base consisting of sentences about the game.
Every sentence has a collection of cells and count of mines in those cells.
Cells, that are known to be safe (we deducted, there can be no mine or we discovered it by playing the cell) are in a separate sentence.
Cells, that are known to be mines (deducted from the knowledge) are in their own sentence as well.
All sentences known about the game consist of AI knowledge base.

By default, the AI player knows how many mines there are in the field. This can be turned off.
By default, the AI player searches for all moves it can do when it gets updated with new knowledge. For performance reasons, this can be turned off, however it usually leads to longer games (in a sense it takes more moves for AI to complete the game).

When the AI player has to make a random move it finds the sentence, where if taken a cell, it has the lowest possibility to be a mine in comparison to other cells in other sentences.

## Possible improvements
Add heuristics to choose moves in a manner, that will allow to win the game in as little moves as possible. (Can even leave out fields, that will bring no new information.)

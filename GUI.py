import argparse
from time import sleep
# from msvcrt import getch

import copy
import sudoku as sud

# import ttk
# import Tkinter
from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
from Tkinter import *

import random

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

# LARGE_FONT= ("Verdana", 12)
# NORM_FONT = ("Helvetica", 10)
# SMALL_FONT = ("Helvetica", 8)

class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """
    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1
    	# self.__popupmsg("hi")
        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack()
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH)

        clear_button = Button(self,
                              text="Clear answers",
                              command=self.__clear_answers)
        clear_button.pack(fill=BOTH, side=BOTTOM)
        solve_button = Button(self,
                              text="BEST hint",
                              command = self.__solve)
        solve_button.pack(fill=BOTH, side=BOTTOM)
        hint_better_button = Button(self,
                             text="Better hint",
                             command=self.__better_hint)
        hint_better_button.pack(fill=BOTH, side=BOTTOM)
        hint_button = Button(self,
                              text="Hint",
                              command = self.__hint)
        hint_button.pack(fill=BOTH, side=BOTTOM)
        undoOne = Button(self,
                              text="Undo",
                              command = self.undo)
        undoOne.pack(fill=BOTH, side=BOTTOM)


        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in xrange(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in xrange(9):
            for j in xrange(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "blue"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )

    def __draw_cursor(self):
    	# removes highlighted red region
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    # def __popupmsg(self,msg):
	   #  popup = Tkinter.Tk()
	   #  popup.wm_title("!")
	   #  label = ttk.Label(popup, text=msg, font=NORM_FONT)
	   #  label.pack(side="top", fill="x", pady=10)
	   #  B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
	   #  B1.pack()
	   #  popup.mainloop()

    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 3.5
        x1 = y1 = MARGIN + SIDE * 5.5
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark green", outline="orange"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="victory",
            fill="white", font=("Arial", 24)
        )
    def __draw_mistake(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 3.5
        x1 = y1 = MARGIN + SIDE * 5.5
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="mistake", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="That's a mistake!!", tags="mistake",
            fill="white", font=("Arial", 12)
        )

    def __cell_clicked(self, event):
        if self.game.game_over:
            return
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.puzzle[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):
    	# print(int(event.char))
    	if event.char == u'\uf700':
    		self.row -= 1
    		self.__draw_cursor()
    	if event.char == u'\uf701':
    		self.row += 1
    		self.__draw_cursor()
    	if event.char == u'\uf702':
    		self.col -= 1
    		self.__draw_cursor()
    	if event.char == u'\uf703':
    		self.col += 1
    		self.__draw_cursor()
    	if event.char == '\x7f':
    		self.game.puzzle[self.row][self.col] = 0
    		self.__draw_puzzle()
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "123456789":
            self.game.puzzle[self.row][self.col] = int(event.char)
            if sud.checkMistake(self.game.puzzle) == True:
                self.game.lastLoc = [self.row,self.col]
                self.__draw_puzzle()
            	self.__draw_mistake()

            	# self.__draw_cursor()
            	# sleep(2)
            	# self.canvas.delete("mistake")

            else:# print("MISTAKE")
	            self.__draw_puzzle()
	            self.__draw_cursor()
	            if self.game.check_win():
	            	self.col, self.row = -10,-10
	            	self.__draw_cursor()
	                self.__draw_victory()

    def undo(self):
        if(len(self.game.lastLoc) > 0):
            row,col = self.game.lastLoc[0],self.game.lastLoc[1]
            self.game.puzzle[row][col] = 0
            self.canvas.delete("mistake")
        self.__draw_puzzle()


    def __clear_answers(self):
        self.game.start()
        self.canvas.delete("victory")
        self.canvas.delete("mistake")
        self.__draw_puzzle()

    def __solve(self):
    	# print("we need to figure this out")
    	# self.game.puzzle = sud.sudoku_solver(self.game.puzzle)
    	sol = sud.sudoku_solver(self.game.puzzle)
    	if sol != None:
    		self.game.puzzle = sol

    	self.__draw_puzzle()
    	if self.game.check_win():
            self.__draw_victory()

    def __hint(self):
    	sol = sud.one_step(self.game.puzzle)
    	if sol != None:
    		self.game.puzzle = sol

    	self.__draw_puzzle()
    	if self.game.check_win():
            self.__draw_victory()
    	# print(hint)

    def __better_hint(self):
        sol = sud.get_best_hint(self.game.puzzle)
        if sol == None:
            return
        
    	self.game.puzzle[sol[1]][sol[2]] = sol[0]
        
    	self.__draw_puzzle()
    	if self.game.check_win():
            self.__draw_victory()

class SudokuBoard(object):
    """
    Sudoku Board representation
    """
    def __init__(self, board_file):
        self.board = self.__create_board(board_file)

    def __create_board(self, board_file):
        board = []
        for line in board_file:
            line = line.strip()
            if len(line) != 9:
                raise SudokuError(
                    "Each line in the sudoku puzzle must be 9 chars long."
                )
            board.append([])

            for c in line:
                if not c.isdigit():
                    raise SudokuError(
                        "Valid characters for a sudoku puzzle must be in 0-9"
                    )
                board[-1].append(int(c))

        if len(board) != 9:
            raise SudokuError("Each sudoku puzzle must be 9 lines long")
        return board


class SudokuGame(object):
    """
    A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    """
    def __init__(self, board_file):
        self.board_file = board_file
        self.start_puzzle = SudokuBoard(board_file).board

    def start(self):
        self.game_over = False
        self.lastLoc = []
        # self.lastNum = 0
        self.puzzle = []
        for i in xrange(9):
            self.puzzle.append([])
            for j in xrange(9):
                self.puzzle[i].append(self.start_puzzle[i][j])

    def check_win(self):
        for row in xrange(9):
            if not self.__check_row(row):
                return False
        for column in xrange(9):
            if not self.__check_column(column):
                return False
        for row in xrange(3):
            for column in xrange(3):
                if not self.__check_square(row, column):
                    return False
        self.game_over = True
        return True

    def __check_block(self, block):
        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])

    def __check_column(self, column):
        return self.__check_block(
            [self.puzzle[row][column] for row in xrange(9)]
        )

    def __check_square(self, row, column):
        return self.__check_block(
            [
                self.puzzle[r][c]
                for r in xrange(row * 3, (row + 1) * 3)
                for c in xrange(column * 3, (column + 1) * 3)
            ]
        )


if __name__ == '__main__':
    # board_name = parse_arguments()

    choice = ""

    def commandEasy():
        global choice
        choice = "easy"
        root.destroy()
    def commandMed():
        global choice
        choice = "medium"
        root.destroy()
    def commandHard():
        global choice
        choice = "hard" 
        root.destroy()

    board_name = "debug"

   

    root = Tk()
    root.canvas = Canvas(width=WIDTH, height=HEIGHT)

    button = Button(root, text="Easy", command=commandEasy)
    button.pack()
    button = Button(root, text="Medium", command=commandMed)
    button.pack()
    button = Button(root, text="Hard", command=commandHard)
    button.pack()

    root.mainloop()

    fileNum = random.randint(1,10)
    print(fileNum)

    path = choice + "/" + choice + str(fileNum) + ".txt"
    print(path)





    root = Tk()

    boards_file = open(path, 'r')
    print(boards_file)
    game = SudokuGame(boards_file)
    game.start()



    SudokuUI(root, game)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.mainloop()

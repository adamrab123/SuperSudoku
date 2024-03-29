from collections import Counter
from copy import deepcopy

def determinePossibilities(grid):
    rows = []
    for i in range(len(grid)):
        rows.append(determine_rows(grid, i))

    cols = []
    for i in range(len(grid)):
        cols.append(determine_cols(grid, i))

    squares = []
    for i in range(3):
        temp = []
        for j in range(3):
            data = []
            for m in range(i*3, (i+1)*3):
                for n in range(j*3, (j+1)*3):
                    if grid[m][n] != 0:
                        data.append(grid[m][n])
            temp.append(data)
        squares.append(temp)

    l = [1,2,3,4,5,6,7,8,9]
    pos = []
    for i in range(len(grid)):
        temp = []
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                r = rows[i]
                c = cols[j]
                s = squares[int(i / 3)][int(j / 3)]
                lis = list(set(r) | set(c) | set(s))
                temp.append([x for x in l if x not in lis])
            else:
                temp.append([])
        pos.append(temp)
    return pos


def check_dups(l):
    counts = Counter()
    for cell in l:
        if cell != 0: counts[cell] += 1
        if cell > 9 or counts[cell] > 1: return False
    return True

def check_sudoku(grid):
    if len(grid) != 9: return False
    if sum(len(row) == 9 for row in grid) != 9: return False
    for row in grid:
        if not check_dups(row): return False
    return True

def determine_rows(grid, i):
    ret = []
    for j in grid[i]:
        if j != 0:
            ret.append(j)
    return ret

def determine_cols(grid, i):
    ret = []
    for j in range(len(grid)):
        if grid[j][i] != 0:
            ret.append(grid[j][i])
    return ret

def sudoku_solver(grid):
    solved_grid = solve(grid)
    return solved_grid

def solve(grid):
    while not solved(grid):
        pos = determinePossibilities(grid)
        # first look for positions that only have 1 possibility
        updated = False

        if check_sudoku(grid) == False:
            return None

        for i in range(len(grid)):
            for j in range(len(grid)):
                if len(pos[i][j]) == 0 and grid[i][j] == 0:
                    return None
                if len(pos[i][j]) == 1:
                    grid[i][j] = pos[i][j][0]
                    updated = True
        if not updated:
            # check one path...
            for i in range(len(grid)):
                for j in range(len(grid)):
                    if grid[i][j] == 0:
                        for xxx in pos[i][j]:
                            grid[i][j] = xxx
                            temp = solve(grid)
                            if temp:
                                return grid
                            else:
                                grid[i][j] = 0
    return grid

def one_step(grid):
    pos = determinePossibilities(grid)
    if check_sudoku(grid) == False:
        return None # means that inputted grid is bad

    for i in range(len(grid)):
        for j in range(len(grid)):
            if len(pos[i][j]) == 0 and grid[i][j] == 0:
                return None # means that inputted grid is bad
            if len(pos[i][j]) == 1:
                grid[i][j] = pos[i][j][0]
                return grid

    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                print(pos[i][j])
                for xxx in pos[i][j]:
                    grid[i][j] = xxx
                    temp = solve(grid)
                    if check_sudoku(temp):
                        return grid
                grid[i][j] = 0

    return grid



def solved(grid):
    for x in grid:
        for y in x:
            if y == 0:
                return False
    return True

def get_best_hint(grid):
    if check_sudoku(grid) == False:
        return False  # means that inputted grid is bad
    frequency = {x: 0 for x in range(1, 10)}
    for row in grid:
        for num in row:
            if num != 0:
                frequency[num] = frequency[num] + 1

    least_frequent_number = min(frequency, key=frequency.get)

    temp = solve(deepcopy(grid))
    for i in range(len(temp)):
        for j in range(len(temp[i])):
            if least_frequent_number == temp[i][j] and grid[i][j] != least_frequent_number:
                return (least_frequent_number, i, j)
    return None



def get_hint(grid):
    pos = determinePossibilities(grid)
    if check_sudoku(grid) == False:
        return False # means that inputted grid is bad

    for i in range(len(grid)):
        for j in range(len(grid)):
            if len(pos[i][j]) == 0 and grid[i][j] == 0:
                return False # means that inputted grid is bad
            if len(pos[i][j]) == 1:
                grid[i][j] = pos[i][j][0]
                return (i,j)

    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                print(pos[i][j])
                for xxx in pos[i][j]:
                    grid[i][j] = xxx
                    temp = solve(grid)
                    if check_sudoku(temp):
                        return (i,j)
                grid[i][j] = 0

    return None

def getColumn(grid,i):
    sol = []
    for row in grid:
        sol.append(row[i])
    return sol

def checkMistake(grid):
    for row in grid:
        for num in list(range(1,10)):
            count = row.count(num)
            if count > 1:
                return True
    for i in range(len(grid)):
        column = getColumn(grid,i)
        # print(column)
        for num in list(range(1,10)):
            count = column.count(num)
            if count > 1:
                return True
    for i in list(range(0,9,3)):
        for j in list(range(0,9,3)):
            box = []
            box.append(grid[i][j])
            box.append(grid[i][j+1])
            box.append(grid[i][j+2])
            box.append(grid[i+1][j])
            box.append(grid[i+1][j+1])
            box.append(grid[i+1][j+2])
            box.append(grid[i+2][j])
            box.append(grid[i+2][j+1])
            box.append(grid[i+2][j+2])
            for num in list(range(1,10)):
                count = box.count(num)
                if count > 1:
                    return True

    return False


example_sudoku = [
    [0, 0, 0, 0, 0, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 7, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

print(checkMistake(example_sudoku))
# prit(getColumn(example_sudoku,0))

# solution = sudoku_solver(example_sudoku)
# solution = one_step(example_sudoku)

# solving = example_sudoku
# while not solved(solving):
#     solving = one_step(solving)

# print(solution)


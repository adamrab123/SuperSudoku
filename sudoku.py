

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
        pos = determinePossiblities(grid)
        # first look for positions that only have 1 possibility
        updated = False
        for i in range(len(grid)):
            for j in range(len(grid)):
                if len(pos[i][j]) == 0 and grid[i][j] == 0:
                    return False
                if len(pos[i][j]) == 1:
                    grid[i][j] = pos[i][j][0]
                    updated = True
        if not updated:
            # check one path...
            for i in range(len(grid)):
                for j in range(len(grid)):
                    if grid[i][j] == 0:
                        print(pos[i][j])
                        for xxx in pos[i][j]:
                            grid[i][j] = xxx
                            temp = solve(grid)
                            if temp:
                                return grid
                            else:s
                        grid[i][j] = 0
    return grid

def solved(grid):
    for x in grid:
        for y in x:
            if y == 0:
                return False
    return True

def determinePossiblities(grid):
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


def get_hint(grid):
    return None

grid = [
    [0, 0, 0, 0, 0, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

print(sudoku_solver(grid))

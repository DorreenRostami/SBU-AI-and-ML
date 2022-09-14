d_name = ['U', 'R', 'D', 'L']
d_row = [ -1, 0, 1, 0]
d_col = [ 0, 1, 0, -1]
board = []
row_n = 0 #total number of rows
col_n = 0 #total number of cols
snake = []
apple_count = 0

#get row/col based on current coordinates, direction and max number of rows/cols on the board
def get_co(co, d, max_co): # d = -1 or 0 or 1 , max_cow = row_n or col_n
    if co + d == max_co:
        return 0
    if co + d == -1:
        return max_co - 1
    return co + d

def is_valid(row, col):
    for i in range(len(snake)):
        if row == snake[i][0] and col == snake[i][1]: #is the snake
            return False 
    return True

def DFS(depth, row, col, l):  
    if depth[row][col] == l:
        return (-1, board[row][col] != 0) #true if it's an apple

    for i in range(4):
        adjx = get_co(row, d_row[i], row_n)
        adjy = get_co(col, d_col[i], col_n)
        if(is_valid(adjx, adjy) and (depth[adjx][adjy] == -1 or depth[adjx][adjy] > depth[row][col] + 1)):
            depth[adjx][adjy] = depth[row][col] + 1
            _, apple_found = DFS(depth, adjx, adjy, l)
            if apple_found == True: 
                return (i, True)  #i = the direction which led to the adj cell where an apple was found

    return (-1, False)

def IDS(row, col):
    m = max(col_n, row_n)
    for i in range(1,m//2 + 1): # i = 1, 1+1, ..., m/2
        depth = [[-1 for _ in range(col_n)] for _ in range(row_n)]
        depth[row][col] = 0
        ans = DFS(depth, row, col, i)
        if ans[1] == True: #apple found
            return ans[0] #dir to apple
    
    #no reachable apple right now even though there are apples left
    for i in range(4):
        adjx = get_co(row, d_row[i], row_n)
        adjy = get_co(col, d_col[i], col_n)
        if(is_valid(adjx, adjy)):
            return i #i = random dir that snake can move to


def move_snake(dir_i):
    global board
    global snake
    global apple_count

    destx = get_co(snake[0][0], d_row[dir_i], row_n)
    desty = get_co(snake[0][1], d_col[dir_i], col_n)

    if board[snake[0][0]][snake[0][1]] != 0: #was on apple
        board[snake[0][0]][snake[0][1]] -= 1
        print("ate an apple and went ", end="")
    else: 
        snake.pop(len(snake)-1)

    snake.insert(0, (destx, desty))
    if board[snake[0][0]][snake[0][1]] != 0: #going on apple
        apple_count -= 1
        print("reached an apple when going ", end="")

def snake_can_move():
    for i in range(4):
        adjx = get_co(snake[0][0], d_row[i], row_n)
        adjy = get_co(snake[0][1], d_col[i], col_n)
        for i in range(len(snake)):
            if adjx == snake[i][0] and adjy == snake[i][1]: #is the snake
                break
            if i == len(snake) - 1: #reached the end of snake but it wasn't equal to current adj
                return True
    return False

def main():
    global board
    global row_n
    global col_n
    global snake
    global apple_count

    #board initialization 
    row_n, col_n = [int(num) for num in input().split(",")]
    board = [[0 for _ in range(col_n)] for _ in range(row_n)]

    #snake
    head_row, head_col = [int(num) for num in input().split(",")]
    snake.append((head_row, head_col))

    #apples
    apple_cell_count = int(input())
    for _ in range(apple_cell_count):
        #cell and number of an apple
        row, col, num = [int(num) for num in input().split(",")]
        apple_count += num
        board[row][col] = num

    while(apple_count > 0):
        if not snake_can_move(): # Game Over
            break
        dir_i = IDS(snake[0][0], snake[0][1])
        move_snake(dir_i)
        print(d_name[dir_i])


if __name__ == "__main__":
    main()
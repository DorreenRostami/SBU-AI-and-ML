from colorama import Fore

from ai import *

#check if cell has an insect inside or not (or is out of bounds)
def is_insect(row, col):
    global dim
    global hive 

    if row >= dim or col >= dim or row < 0 or col < 0:
        return 'o' #out of bounds
    elif hive[row][col][0][1] == 'g':
        return 'g' 
    elif hive[row][col][0][1] == 'r':
        return 'r'
    else:
        return 'n' #no insect

#check if cell has any full cell around it
def has_insect_around(row, col):
    global co
    for i in range(len(co)):
        tmp = is_insect(co[i][0] + row, co[i][1] + col)
        if tmp == 'r' or tmp == 'g': #has insect
            return 1
    return 0

#check if this action can be done (based on queen existing)
def check_action(turn):
    global red_ins
    global green_ins

    action = input("move or put: ")
    if action != "move" and action != "put":
        print("enter a valid action")
        return 0
    if action == "move":
        if (turn%2 == 0 and red_ins["Queen"] == 1) or (turn%2 == 1 and green_ins["Queen"] == 1):
            print("You don't have a queen")
            print("enter a valid action")
            return 0
        elif (turn == 6 and red_ins["Queen"] == 1) or (turn == 7 and green_ins["Queen"] == 1):
            print("You have to put the queen on the board now")
            return 0
    return action

def check_ins(ins):
    if ins != 'Queen' and ins != 'Cicada' and ins != 'Beetle' and ins != 'Ant' and ins != 'Spider':
        return 0
    return 1

def check_coordinate(row, col):
    global hive

    if (row%2 == 0 and col%2 == 1) or (row%2 == 1 and col%2 == 0):
        return 0
    return 1

'''
check if insect can be put here (for turn >= 2)
first checks if any insect of the opposing color is around it
then check if cell is occupied + if the selected insect exists off board
if everything is ok, put insect in the cell
if insect was a queen, save it's coordinates
'''
def put_insect(row, col, ins, turn):
    global hive
    global red_ins
    global green_ins
    global red_q
    global green_q 
    global greens_onboard
    global reds_onboard

    for i in range(len(co)):
        if turn%2 == 0 and is_insect(co[i][0] + row, co[i][1] + col) == 'g':
            print("there is a green around here")
            return 0
        elif turn%2 == 1 and is_insect(co[i][0] + row, co[i][1] + col) == 'r':
            print("there is a red around here")
            return 0

    if is_insect(row, col) == 'n': #no insect is here
        if turn%2 == 0: 
            if red_ins[ins] == 0:
                print("You don't have any of this insect left")
                return 0
            if turn == 6 and ins != "Queen" and red_ins["Queen"] == 1: #queen needs to be inside when r_turn <= 4
                print("put the queen on the board")
                return 0

            hive[row][col].insert(0, " r," + ins[0] + " ")
            red_ins[ins] -= 1
            reds_onboard.append([row, col])
            if ins == "Queen":
                red_q = [row, col]
        else:
            if green_ins[ins] == 0:
                print("You don't have any of this insect left")
                return 0
            if turn == 7 and ins != "Queen" and green_ins["Queen"] == 1: #queen needs to be inside when g_turn <= 4
                print("put the queen on the board")
                return 0

            hive[row][col].insert(0, " g," + ins[0] + " ")
            green_ins[ins] -= 1
            greens_onboard.append([row, col])
            if ins == "Queen":
                green_q = [row, col]
            
        return 1
    else:
        print("can't put insect here")
        return 0

#funcs for checking if removing insect disconnects hive
def hive_dfs(row, col, visited, cnt_visited = 1):
    global hive
    global co

    visited[row][col] = 1
    for i in range(len(co)):
        r = co[i][0] + row
        c = co[i][1] + col
        is_ins = is_insect(r, c)
        if (is_ins == 'r' or is_ins == 'g') and visited[r][c] == 0: #has unvisited insect
            cnt_visited += len(hive[r][c]) - 1
            cnt_visited = hive_dfs(r, c, visited, cnt_visited)
    return cnt_visited

def is_bridge(row, col):
    global hive
    global dim
    global co
    global red_ins
    global green_ins

    if(len(hive[row][col]) > 2): #insects on top of eachother
        return 0

    moving_ins = hive[row][col].pop(0) #remove ins temporarily
    
    visited = []
    for _ in range(dim):
        visited. append([0 for _ in range(dim)])

    for i in range(len(co)):
        tmp = is_insect(co[i][0] + row, co[i][1] + col)
        if  tmp == 'r' or tmp == 'g': #has insect
            cnt_visited = hive_dfs(co[i][0] + row, co[i][1] + col, visited) + 1 #1 = the insect we're moving
            cnt_onboard = 22 - sum(red_ins.values()) - sum(green_ins.values()) #all - off the board
            hive[row][col].insert(0, moving_ins)
            return 0 if cnt_visited == cnt_onboard else 1

'''
func to check whether the insect can move to the next cell
used for Queens, Spiders and Ants since they move on the ground
returns false the entry point is very small
'''
def can_enter(src_row, src_col, dst_row, dst_col):
    global hive
    row_diff = dst_row - src_row
    col_diff = dst_col - src_col
    tmp1 = False
    tmp2 = False
    if col_diff == 0:
        if row_diff > 0: #moving down
            tmp1 = is_insect(src_row + 1, src_col + 1)
            tmp2 = is_insect(src_row + 1, src_col - 1)            
        else: #row_diff < 0, moving up
            tmp1 = is_insect(src_row - 1, src_col + 1)
            tmp2 = is_insect(src_row - 1, src_col - 1)
    elif col_diff < 0: 
        if row_diff > 0:
            tmp1 = is_insect(src_row + 2, src_col)
            tmp2 = is_insect(src_row - 1, src_col - 1)
        else:
            tmp1 = is_insect(src_row - 2, src_col)
            tmp2 = is_insect(src_row + 1, src_col - 1)
    else: #col_diff > 0
        if row_diff > 0:
            tmp1 = is_insect(src_row + 2, src_col)
            tmp2 = is_insect(src_row - 1, src_col + 1)
        else:
            tmp1 = is_insect(src_row - 2, src_col)
            tmp2 = is_insect(src_row + 1, src_col + 1)
    print(src_row, "  ", src_col)
    print(tmp1, "    ", tmp2)
    if tmp1 == 'n' or tmp2 == 'n': #atleast one is empty
        return True
    return False

#func for moving insects from
def move_ins(src_row, src_col, dst_row, dst_col, ins_co = []):
    global hive
    global co
    global reds_onboard
    global greens_onboard

    if is_insect(dst_row, dst_col) == 'o':
        print("destination out of bounds")
        return 0

    if is_bridge(src_row, src_col) == 1:
        print("moving this insect disconnects the hive")
        return 0

    ins = hive[src_row][src_col][0]

    if ins[3] == 'Q': #Queen
        if is_insect(dst_row, dst_col) != 'n':
            print("invalid destination")
            return 0
        if has_insect_around(dst_row, dst_col) == 0:
            print("destination is not connected to hive")
            return 0
        if not can_enter(src_row, src_col, dst_row, dst_col):
            print("unable to move to destination")
            return 0
        for i in range(len(co)):
            if dst_row == co[i][0] + src_row and dst_col == co[i][1] + src_col:
                hive[dst_row][dst_col].insert(0, ins)
                hive[src_row][src_col].pop(0)
                if ins[1] == 'r':
                    red_q.remove([src_row, src_col])
                    red_q.append([dst_row, dst_col])
                else:
                    green_q.remove([src_row, src_col])
                    green_q.append([dst_row, dst_col])
        print("Queens can only move 1 cell around")
        return 0
    elif ins[3] == 'B': #Beetle 
        if is_insect(dst_row,dst_col) == 'n' and has_insect_around(dst_row, dst_col) == 0:
            print("destination is not connected to hive")
            return 0
        for i in range(len(co)):
            if dst_row == co[i][0] + src_row and dst_col == co[i][1] + src_col:
                hive[dst_row][dst_col].insert(0, ins)
                hive[src_row][src_col].pop(0)
        print("Beetles can only move 1 cell around")
        return 0
    elif ins[3] == 'C': #Cicada
        if has_insect_around(dst_row, dst_col) == 0:
            print("destination is not connected to hive")
            return 0
        tmp_row = src_row
        tmp_col = src_col
        row_diff = dst_row - src_row
        col_diff = dst_col - src_col
        r = 2
        c = 0
        if col_diff == 0:
            if row_diff < 0:
                r = -2
        else:
            r = 1 if row_diff > 0 else -1
            c = 1 if col_diff > 0 else -1
        if abs(row_diff) == abs(col_diff) or col_diff == 0: #moving on diameter or column
            while tmp_row != dst_row:
                tmp_row += r
                tmp_col += c
                if is_insect(tmp_row, tmp_col) == 'n': #will never be 'o'
                    if tmp_row != dst_row: #a hole has been seen and cicada hasn't reached dest
                        print("there is an empty cell in the way")
                        return 0
            hive[dst_row][dst_col].insert(0, ins)
            hive[src_row][src_col].pop(0)
        else:
            print("Cicadas can only move on a line")
            return 0
    elif ins[3] == 'A': #Ant
        hive[src_row][src_col].pop(0) #because when we want to check has_insect_around in each step, this would also count
        for i in range(len(ins_co)-1): 
            tmp = is_insect(ins_co[i+1][0], ins_co[i+1][1])
            if  tmp == 'g' or tmp == 'r':
                print("There is an insect on your way")
                hive[src_row][src_col].insert(0, ins)
                return 0

            row_diff = abs(ins_co[i][0] - ins_co[i+1][0])
            col_diff = abs(ins_co[i][1] - ins_co[i+1][1])
            if not(row_diff == 1 and col_diff == 1) and not(row_diff == 2 and col_diff == 0):
                print("invalid movement")
                hive[src_row][src_col].insert(0, ins)
                return 0
            if has_insect_around(ins_co[i+1][0], ins_co[i+1][1]) == 0:
                print("your movement is not clinging to the wall")
                hive[src_row][src_col].insert(0, ins)
                return 0
            if not can_enter(ins_co[i][0], ins_co[i][1], ins_co[i+1][0], ins_co[i+1][1]):
                print("unable to move to destination")
                hive[src_row][src_col].insert(0, ins)
                return 0
        hive[dst_row][dst_col].insert(0, ins)  
    elif ins[3] == 'S': #Spider
        hive[src_row][src_col].pop(0)
        if (ins_co[1] == ins_co[2]) or (ins_co[2] == ins_co[3]) or (ins_co[1] == ins_co[3]):
            print("same coordinates have been entered")
            hive[src_row][src_col].insert(0, ins)
            return 0
        for i in range(len(ins_co)-1):
            tmp = is_insect(ins_co[i+1][0], ins_co[i+1][1])
            if  tmp == 'g' or tmp == 'r':
                print("There is an insect on your way")
                hive[src_row][src_col].insert(0, ins)
                return 0

            row_diff = abs(ins_co[i][0] - ins_co[i+1][0])
            col_diff = abs(ins_co[i][1] - ins_co[i+1][1])
            if not(row_diff == 1 and col_diff == 1) and not(row_diff == 2 and col_diff == 0):
                print("invalid movement")
                hive[src_row][src_col].insert(0, ins)
                return 0
            if has_insect_around(ins_co[i+1][0], ins_co[i+1][1]) == 0:
                print("your movement is not clinging to the wall")
                hive[src_row][src_col].insert(0, ins)
                return 0
            if not can_enter(ins_co[i][0], ins_co[i][1], ins_co[i+1][0], ins_co[i+1][1]):
                print("unable to move to destination")
                hive[src_row][src_col].insert(0, ins)
                return 0
        hive[dst_row][dst_col].insert(0, ins)
    
    if ins[1] == 'r':
        reds_onboard.remove([src_row, src_col])
        reds_onboard.append([dst_row, dst_col])
    else:
        greens_onboard.remove([src_row, src_col])
        greens_onboard.append([dst_row, dst_col])
    return 1
        
def check_can_put(turn):
    global reds_onboard
    global greens_onboard
    global hive
    global co


    main_onboard = reds_onboard if turn % 2 == 0 else greens_onboard
    op_color = 'g' if turn % 2 == 0 else 'r'

    if len(main_onboard) == 11:
        return 0
    elif len(main_onboard) == 0:
        return 1
    
    for i in range(len(main_onboard)):
        for j in range(len(co)):
            row = co[j][0] + main_onboard[i][0]
            col = co[j][1] + main_onboard[i][1]
            tmp = is_insect(row, col)
            if tmp == 'n':
                for k in range(len(co)):
                    tmp2 = is_insect(row + co[k][0], col + co[k][1])
                    if tmp2 == op_color:
                        break
                    elif k == len(co) -1:
                        return 1

    return 0

def check_can_move(turn):
    global reds_onboard
    global greens_onboard
    global hive
    global co

    main_onboard = reds_onboard if turn % 2 == 0 else greens_onboard

    for i in range(len(main_onboard)):
        row = main_onboard[i][0]
        col = main_onboard[i][1]
        if not is_bridge(row, col):
            ins = hive[row][col].pop(0)
            if ins[3] == 'C' or ins[3] == 'B':
                hive[row][col].insert(0, ins) 
                return 1
            for j in range(len(co)):
                row2 = co[j][0] + row
                col2 = co[j][1] + col
                if has_insect_around(row2, col2):
                    if can_enter(row, col, row2, col2):
                        hive[row][col].insert(0, ins)
                        return 1      
            hive[row][col].insert(0, ins)
    return 0
        
def who_wins():
    global hive
    global green_q
    global red_q
    global co

    r_win = 2
    g_win = 2

    if red_q:
        for i in range(len(co)):
            counter = 0
            tmp = is_insect(co[i][0] + red_q[0], co[i][1] + red_q[1])
            if not(tmp == 'r' or tmp == 'g'): #a cell with no insect is around the red queen
                counter += 1
        if counter == 6:
            g_win = 1
    
    if green_q:
        for i in range(len(co)):
            counter = 0
            tmp = is_insect(co[i][0] + green_q[0], co[i][1] + green_q[1])
            if not(tmp == 'r' or tmp == 'g'): #a cell with no insect is around the green queen
                counter += 1
        if counter == 6:
            r_win = 1

    if g_win == 1 or r_win == 1:
        if g_win == 1 and r_win == 1:
            print("The score is equal")           
        elif g_win == 1:
            print("Player green wins")
        else:
            print("Player red wins")
        return 1
    return 0

#func for printing hive
def print_board(hive):
    for i in range(dim):
        for j in range(dim):
            if (i%2==0 and j%2==0) or (i%2==1 and j%2==1):
                if hive[i][j][0][1] == 'r':
                    print(Fore.RED + hive[i][j][0], end=" ")
                elif hive[i][j][0][1] == 'g':
                    print(Fore.GREEN + hive[i][j][0], end=" ")
                else:
                    print(Fore.WHITE + hive[i][j][0], end=" ")
            else:
                print("     ", end=" ")
        print()
    print(Fore.WHITE + "--------------------------------")


dim = 10 #max 100 if you want the visual representation of the hive to be clean
'''
hive is a 3d list with the first 2 dimensions being row and col, 
3rd dimension being the number or insect shown on board
by putting the first insect, hive[r][c][0] = insect, hive[r][c][1] = r,c
element 0 in the 3rd dimension always shows what we see from the top
'''
hive = [] 
red_ins = {"Queen": 1, "Beetle": 2, "Cicada": 3, "Spider": 2, "Ant": 3} #red's insects off board 
green_ins = {"Queen": 1, "Beetle": 2, "Cicada": 3, "Spider": 2, "Ant": 3} #green's insects off board
red_q = [] #coordinates for the red queen
green_q = [] #coordinates for the green queen
greens_onboard = []
reds_onboard = []
co = [[1,1], [1,-1], [-1,1], [-1,-1], [2,0], [-2,0]] #coordinates for checking neighbors

def main():
    global hive
    global red_ins
    global green_ins
    global red_q
    global green_q 
    global greens_onboard
    global reds_onboard
    global co
    global dim

    turn = 0 # even numbers red, odd numbers green
    
    for r in range(dim):
        hive.append([['{s:{p}^{n}}'.format(s="{},{}".format(r,c),n=5,p=' ') for _ in range(1)] for c in range(dim)])

    print_board(hive)


    while True:
        if check_can_put(turn) == 0 and check_can_move(turn) == 0:
            turn += 1
            continue

        print('red') if turn % 2 == 0 else print('green')

        #red's turn (AI)
        print("turn ", turn)
        if turn%2 == 0:
            _, move = minimax(turn, 4, True, hive, red_ins, green_ins, red_q, green_q, 
                reds_onboard, greens_onboard, -inf, inf)
            ins = "Queen"
            if move[0] == 'B':
                ins = "Beetle"
            elif move[0] == 'S':
                ins = "Spider"
            elif move[0] == 'C':
                ins = "Cicada"
            elif move[0] == 'A': 
                ins = "Ant"
            if move[1] != None:
                hive[move[1][0]][move[1][1]].pop(0)
            
            if move[0] == 'Q':
                red_q = [move[2][0],move[2][1]]
            hive[move[2][0]][move[2][1]].insert(0, " r," + ins[0] + " ")

            if move[1] == None:
                red_ins[ins] -= 1
                reds_onboard.append([move[2][0],move[2][1]])
            turn += 1

        elif turn <= 1:
            print("choose where to put what insect")
            row = int(input("row: "))
            col = int(input("col: "))
            if check_coordinate(row, col) == 0:
                print("not a valid coordinate has been entered")
                continue
            ins = input("insect: ")
            if check_ins(ins) == 0:
                print("invalid insect")
                continue
            # if turn == 0:
            #     hive[row][col].insert(0, " r," + ins[0] + " ")
            #     red_ins[ins] -= 1
            #     if ins == "Queen":
            #         red_q = [row, col]
            #     reds_onboard.append([row, col])
            #     turn += 1
            elif turn == 1:
                for i in range(len(co)):
                    if is_insect(co[i][0] + row, co[i][1] + col) == 'r':
                        hive[row][col].insert(0, ' g,' + ins[0] + ' ')
                        green_ins[ins] -= 1
                        if ins == "Queen":
                            green_q = [row, col]
                        greens_onboard.append([row, col])
                        turn += 1
                        break
        #turn >= 2
        else:
            action = check_action(turn)
            if action == 0:
                continue
            elif action == "put":
                row = int(input("row: "))
                col = int(input("col: "))
                if check_coordinate(row, col) == 0:
                    print("not a valid coordinate has been entered")
                    continue
                ins = input("insect: ")
                if check_ins(ins) == 0:
                    print("invalid insect")
                    continue
                can_put = put_insect(row, col, ins, turn)
                turn = turn + 1 if can_put else turn
            else:
                src_row = int(input("source row: "))
                src_col = int(input("source col: "))
                if check_coordinate(src_row, src_col) == 0:
                    print("not a valid coordinate has been entered")
                    continue
                # different input for Ant and Spider
                if hive[src_row][src_col][0][3] == 'A':
                    ant_co = []
                    ant_co.append([src_row, src_col])
                    number_of_moves = int(input("enter number of moves you want to make: "))
                    for i in range(number_of_moves):
                        row = int(input("row {}: ".format(i)))
                        col = int(input("col {}: ".format(i)))
                        if check_coordinate(row, col) == 0:
                            print("not a valid coordinate has been entered")
                            i -= 1
                            continue
                        ant_co.append([row, col])
                    moved = move_ins(src_row, src_col, ant_co[number_of_moves][0], ant_co[number_of_moves][1], ant_co)
                    turn = turn + 1 if moved else turn
                elif hive[src_row][src_col][0][3] == 'S':
                    spider_co = []
                    spider_co.append([src_row, src_col])
                    print("enter 3 moves in order: ")
                    for i in range(3):
                        row = int(input("row {}: ".format(i)))
                        col = int(input("col {}: ".format(i)))
                        if check_coordinate(row, col) == 0: ############################################3
                            print("not a valid coordinate has been entered")
                            i -= 1
                            continue
                        spider_co.append([row, col])
                    moved = move_ins(src_row, src_col, spider_co[3][0], spider_co[3][1], spider_co)
                    turn = turn + 1 if moved else turn
                elif hive[src_row][src_col][0][3] == 'Q' or hive[src_row][src_col][0][3] == 'B' or hive[src_row][src_col][0][3] == 'C':
                    dest_row = int(input("dest row: "))
                    dest_col = int(input("dest col: "))
                    if check_coordinate(dest_row, dest_col) == 0:
                        print("not a valid coordinate has been entered")
                        continue
                    moved = move_ins(src_row, src_col, dest_row, dest_col)
                    turn = turn + 1 if moved else turn
                else:
                    print("no insect exists in source")
                    continue        

        if who_wins() == 1:
            print_board(hive)
            break
        
        # os.system("cls")
        print_board(hive)

if __name__ == "__main__":
    main()
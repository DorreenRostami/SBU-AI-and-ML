from cmath import inf
from copy import deepcopy
import random
import hive

mid_row = hive.dim // 2 - 1
mid_col = hive.dim // 2 - 1
co = [[1,1], [1,-1], [-1,1], [-1,-1], [2,0], [-2,0]] #coordinates for checking neighbors

def is_insect(row, col, board):
    dim = hive.dim

    if row >= dim or col >= dim or row < 0 or col < 0:
        return 'o' #out of bounds
    elif board[row][col][0][1] == 'g':
        return 'g' 
    elif board[row][col][0][1] == 'r':
        return 'r'
    else:
        return 'n' #no insect

#check if cell has any enemy around it
def has_enemy_around(row, col, board, enemy):
    for i in range(len(co)):
        tmp = is_insect(co[i][0] + row, co[i][1] + col, board)
        if tmp == enemy:
            return 1
    return 0


def available_moves(board, turn, red_ins, green_ins, red_q, green_q, 
        reds_onboard, greens_onboard):
    
    moves = []
    if turn == 0:
        for i in ['S', 'C', 'B']:
            moves.append([i, None, (mid_row,mid_col)])
    elif turn == 1:
        for i in ['S', 'C', 'B']:
            for j in range(len(co)):
                moves.append([i, None, (mid_row+co[j][0],mid_col+co[j][1])])

    elif turn == 2: #red's 2nd time
        for i in range(len(co)):
            row = mid_row+co[i][0]
            col = mid_col+co[i][1]
            if is_insect(row, col, board) != 'n':
                continue
            if has_enemy_around(row, col, board, 'g') == 0:
                moves.append(['Q', None, (row,col)])
                moves.append(['S', None, (row,col)])
    
    elif turn == 3: #green's 2nd time
        for cc in range(len(co)):
            roww = mid_row+co[cc][0]
            coll = mid_col+co[cc][1]
            tmp = is_insect(co[cc][0] + roww, co[cc][1] + coll, board)
            if tmp == 'g': #found where the first green was put
                for i in range(len(co)):
                    row = roww+co[i][0]
                    col = coll+co[i][1]
                    if is_insect(row, col, board) != 'n':
                        continue
                    if has_enemy_around(row, col, board, 'r') == 0:
                        if green_ins["Queen"] == 1: #if human player didn't put Queen on their 1st turn
                            moves.append(['Q', None, (row,col)])
                        moves.append(['S', None, (row,col)])
                break

    elif turn == 4: #red's 3rd time
        for r in range(len(reds_onboard)):
            roww = reds_onboard[r][0]
            coll = reds_onboard[r][1]
            for i in range(len(co)):
                row = roww+co[i][0]
                col = coll+co[i][1]
                if is_insect(row, col, board) != 'n':
                    continue
                if has_enemy_around(row, col, board, 'g') == 0:
                    if red_ins["Queen"] == 1:
                        moves.append(['Q', None, (row,col)])
                    if red_ins["Beetle"] > 0:
                        moves.append(['B', None, (row,col)])
                    if red_ins["Spider"] > 0:
                        moves.append(['S', None, (row,col)])

    elif turn == 5: #green's 3rd time
        for g in range(len(greens_onboard)):
            roww = greens_onboard[g][0]
            coll = greens_onboard[g][1]
            for i in range(len(co)):
                row = roww+co[i][0]
                col = coll+co[i][1]
                if is_insect(row, col, board) != 'n':
                    continue
                if has_enemy_around(row, col, board, 'r') == 0:
                    if green_ins["Queen"] == 1:
                        moves.append(['Q', None, (row,col)])
                    if green_ins["Beetle"] > 0:
                        moves.append(['B', None, (row,col)])
                    if green_ins["Spider"] > 0:
                        moves.append(['S', None, (row,col)])

    elif turn == 6: #red's 4th time
        for r in range(len(reds_onboard)):
            roww = reds_onboard[r][0]
            coll = reds_onboard[r][1]
            for i in range(len(co)):
                row = roww+co[i][0]
                col = coll+co[i][1]
                if is_insect(row, col, board) != 'n':
                    continue
                if has_enemy_around(row, col, board, 'g') == 0:
                    if green_ins["Queen"] == 1:
                        moves.append(['Q', None, (row,col)])
                    else:
                        if green_ins["Beetle"] > 0:
                            moves.append(['B', None, (row,col)])
                        if green_ins["Spider"] > 0:
                            moves.append(['S', None, (row,col)])
                        if green_ins["Ant"] > 0:
                            moves.append(['A', None, (row,col)])

    elif turn == 7: #green's 4th time
        for g in range(len(greens_onboard)):
            roww = greens_onboard[g][0]
            coll = greens_onboard[g][1]
            for i in range(len(co)):
                row = roww+co[i][0]
                col = coll+co[i][1]
                if is_insect(row, col, board) != 'n':
                    continue
                if has_enemy_around(row, col, board, 'r') == 0:
                    if green_ins["Queen"] == 1:
                        moves.append(['Q', None, (row,col)])
                    else:
                        if green_ins["Beetle"] > 0:
                            moves.append(['B', None, (row,col)])
                        if green_ins["Spider"] > 0:
                            moves.append(['S', None, (row,col)])
                        if green_ins["Ant"] > 0:
                            moves.append(['A', None, (row,col)])
    
    else: #mid game
        available_cells = []
        friends_onboard = reds_onboard
        enemy = 'g'
        friends_ins = red_ins
        if turn%2==1: #red 
            friends_onboard = greens_onboard
            enemy = 'r'
            friends_ins = green_ins
        
        for ins in friends_onboard:
            ins_row = ins[0]
            ins_col = ins[1]
            for i in range(len(co)):
                row = ins_row + co[i][0]
                col = ins_col + co[i][1]
                if is_insect(row, col, board) != 'n':
                    continue
                if has_enemy_around(row, col, board, enemy) == 0:
                    available_cells.append([row,col])
        
        for cell in available_cells:
            if friends_ins["Beetle"] > 0:
                moves.append(['B', None, (cell[0],cell[1])])
            if friends_ins["Cicada"] > 0:
                moves.append(['C', None, (cell[0],cell[1])])
            if friends_ins["Spider"] > 0:
                moves.append(['S', None, (cell[0],cell[1])])
            if friends_ins["Ant"] > 0:
                moves.append(['A', None, (cell[0],cell[1])])
    
    random.shuffle(moves)
    return moves


def evaluate (turn, board, red_q, green_q):
    around_red = 0
    around_green = 0
    score = 0
    for i in range(len(co)):
        if len(red_q) > 0:
            r = red_q[0] + co[i][0]
            c = red_q[1] + co[i][1]
            ins = is_insect(r, c, board) 
            if ins != 'n' and ins != 'o':
                around_red += 1
        if len(green_q) > 0:
            r = green_q[0] + co[i][0]
            c = green_q[1] + co[i][1]
            ins = is_insect(r, c, board) 
            if ins != 'n' and ins != 'o':
                around_green += 1
    
    if turn%2 == 0: #red
        score = around_green - around_red
    else:
        score = around_red - around_green
    return score

def minimax(turn, depth, maximizing, board, red_ins, green_ins, red_q, green_q, 
        reds_onboard, greens_onboard, alpha, beta):

    color = ' r,' if turn % 2 == 0 else ' g,'

    if depth < 0 : 
        return 0, None
    elif depth == 0:
        return evaluate (turn, board, red_q, green_q), None
    
    new_red_ins = deepcopy(red_ins)
    new_green_ins = deepcopy(green_ins)
    new_red_q = deepcopy(red_q)
    new_green_q = deepcopy(green_q)
    new_reds_onboard = deepcopy(reds_onboard)
    new_greens_onboard = deepcopy(greens_onboard)
    moves = available_moves(board, turn, new_red_ins, new_green_ins, new_red_q, new_green_q, 
        new_reds_onboard, new_greens_onboard)

    if maximizing == 1: #always for red during AI vs human
        best_sib = -inf
        best_move = None
        for move in moves:
            new_board = deepcopy(board)
            if move[1] != None:                                                         # action = move
                new_board[move[1][0]][move[1][1]].pop(0)
                new_board[move[2][0]][move[2][1]].insert(0, color + move[0] + " ")
                #we know it's always red
                new_reds_onboard.append([move[2][0], move[2][1]])
                new_reds_onboard.remove([move[1][0], move[1][1]])
                if move[0] == 'Q':
                    new_red_q = [move[2][0], move[2][1]]
            else:                                                                       # action = put
                print("hi")
                print(move)
                print(move[2])
                new_board[move[2][0]][move[2][1]].insert(0, color + move[0] + " ")
                #we know it's always red
                new_reds_onboard.append([move[2][0], move[2][1]])
                if move[0] == 'Q':
                    new_red_q = [move[2][0], move[2][1]]
                    new_red_ins["Queen"] -= 1
                elif move[0] == 'B':
                    new_red_ins["Beetle"] -= 1
                elif move[0] == 'S':
                    new_red_ins["Spider"] -= 1
                elif move[0] == 'C':
                    new_red_ins["Cicada"] -= 1
                elif move[0] == 'A':
                    new_red_ins["Ant"] -= 1
                

            value, _ = minimax(turn + 1, depth - 1, not maximizing, new_board, new_red_ins, new_green_ins, 
                        new_red_q, new_green_q, new_reds_onboard, new_greens_onboard, alpha, beta)
            if value > best_sib:
                print("max " , turn, " ", move)
                best_sib = value
                best_move = move
            alpha = max(alpha, best_sib)

            if beta <= alpha:
                break
        
        return best_sib, best_move

    else: #always for green during AI vs human
        best_sib = inf
        best_move = None
        for move in moves:
            new_board = deepcopy(board)
            if move[1] != None:                                                         # action = move
                new_board[move[1][0]][move[1][1]].pop(0)
                new_board[move[2][0]][move[2][1]].insert(0, color + move[0] + " ")
                #we know it's always green
                new_greens_onboard.append([move[2][0], move[2][1]])
                new_greens_onboard.remove([move[1][0], move[1][1]])
                if move[0] == 'Q':
                    new_green_q = [move[2][0], move[2][1]]
            else:                                                                       # action = put
                print("hi")
                print(move)
                print(move[2])
                new_board[move[2][0]][move[2][1]].insert(0, color + move[0] + " ")
                #we know it's always green
                new_greens_onboard.append([move[2][0], move[2][1]])
                if move[0] == 'Q':
                    new_green_q = [move[2][0], move[2][1]]
                    new_green_ins["Queen"] -= 1
                elif move[0] == 'B':
                    new_green_ins["Beetle"] -= 1
                elif move[0] == 'S':
                    new_green_ins["Spider"] -= 1
                elif move[0] == 'C':
                    new_green_ins["Cicada"] -= 1
                elif move[0] == 'A':
                    new_green_ins["Ant"] -= 1

            value, _ = minimax(turn + 1, depth - 1, not maximizing, new_board, new_red_ins, new_green_ins, 
                        new_red_q, new_green_q, new_reds_onboard, new_greens_onboard, alpha, beta)
            if value < best_sib:
                print("min " , turn, " ", move)
                best_sib = value
                best_move = move
            beta = min(beta, best_sib)

            if beta <= alpha:
                break

        return best_sib, best_move
"""
Gomoku

Author: Thomas Culham.  Last modified: Nov. 26, 2020

"""

def is_empty(board):
    for i in board:
        for j in i:
            if(j!=" "):
                return False
    return True





def is_bounded(board, y, x, l, dy, dx):


    if(loc_exists(board,x+dx,y+dy," ") and loc_exists(board,x-(l*dx),y-(l*dy)," ")):
        return "OPEN"
    elif(loc_exists(board,x+dx,y+dy," ") or loc_exists(board,x-(l*dx),y-(l*dy)," ")):
        return "SEMIOPEN"
    else:
        return "CLOSED"



def loc_exists(board, x,y,s):
    if(x<len(board) and y<len(board) and x>-1 and y>-1):
        if(board[y][x]==s ):
            return True
    return False



def detect_row(board, col, y, x, l, dy, dx):
    o=0
    so=0

    if(dy==0 and dx==1):
        count=0
        pcount=0
        for i in range(len(board)):
            if(loc_exists(board,x+i,y,col)):
                count+=1
            else:
                pcount=count
                count=0
            if(pcount==l):
                if(is_bounded(board,0,x+i-1,l,dy,dx)=="OPEN"):
                    o+=1
                if(is_bounded(board,0,x+i-1,l,dy,dx)=="SEMIOPEN"):
                    so+=1
            elif(i==7 and count==l):
                if(is_bounded(board,0,x+i-1,l,dy,dx)=="OPEN"):
                    o+=1
                if(is_bounded(board,0,x+i-1,l,dy,dx)=="SEMIOPEN"):
                    so+=1
            pcount=0




    if(dx==0 and dy==1):
        count=0
        pcount=0
        for i in range(len(board)):
            if(loc_exists(board,x,y+i,col)):
                count+=1
            else:
                pcount=count
                count=0
            if(pcount==l):
                if(is_bounded(board,y+i-1,0,l,dy,dx)=="OPEN"):
                    o+=1
                if(is_bounded(board,y+i-1,0,l,dy,dx)=="SEMIOPEN"):
                    so+=1
            elif(i==7 and count==l):
                if(is_bounded(board,y+i-1,0,l,dy,dx)=="OPEN"):
                    o+=1
                if(is_bounded(board,y+i-1,0,l,dy,dx)=="SEMIOPEN"):
                    so+=1
            pcount=0





    if(dx==-1 and dy==1):
        count=0
        pcount=0
        for i in range(len(board)):
            if(loc_exists(board,x-i,y+i,col)):
                count+=1
            else:
                pcount=count
                count=0
            if(pcount==l):
                if(is_bounded(board,y+i-1,x-i-1,l,dy,dx)=="OPEN"):
                    o+=1
                if(is_bounded(board,y+i-1,x-i-1,l,dy,dx)=="SEMIOPEN"):
                    so+=1
            elif(i==7 and count==l):
                if(is_bounded(board,y+i-1,x-i-1,l,dy,dx)=="OPEN"):
                    o+=1
                if(is_bounded(board,y+i-1,x-i-1,l,dy,dx)=="SEMIOPEN"):
                    so+=1
            pcount=0

    if(dy==1 and dx==1):
        count=0
        pcount=0
        for i in range(len(board)):
            if(loc_exists(board,x+i,y+i,col)):
                count+=1
            else:
                pcount=count
                count=0
            if(pcount==l):
                if(is_bounded(board,y+i-1,x+i-1,l,dy,dx)=="OPEN"):
                    o+=1
                if(is_bounded(board,y+i-1,x+i-1,l,dy,dx)=="SEMIOPEN"):
                    so+=1
            elif(i==7 and count==l):
                if(is_bounded(board,y+i-1,x+i-1,l,dy,dx)=="OPEN"):
                    o+=1
                if(is_bounded(board,y+i-1,x+i-1,l,dy,dx)=="SEMIOPEN"):
                    so+=1
            pcount=0

    return (o,so)






def detect_rows(board, col, length):
    o=0
    so=0
    for i in range(len(board)):
        o+=detect_row(board,col,i,0,length,0,1)[0]
        o+=detect_row(board,col,0,i,length,1,0)[0]
        o+=detect_row(board,col,0,i,length,1,1)[0]
        o+=detect_row(board,col,0,i,length,1,-1)[0]

        if(i<len(board)-1):
            o+=detect_row(board,col,i+1,len(board)-1,length,1,-1)[0]
            so+=detect_row(board,col,i+1,len(board)-1,length,1,-1)[1]
            so+=detect_row(board,col,i+1,0,length,1,1)[1]
            o+=detect_row(board,col,i+1,0,length,1,1)[0]

        so+=detect_row(board,col,i,0,length,0,1)[1]
        so+=detect_row(board,col,0,i,length,1,0)[1]
        so+=detect_row(board,col,0,i,length,1,1)[1]
        so+=detect_row(board,col,0,i,length,1,-1)[1]
    return (o,so)






def search_max(board):
    pass
    high_score=0
    ans=(0,0)
    b=board.copy()
    for i in range(len(b)):
        for j in range(len(b)):
            if(b[i][j]==" "):
                b[i][j]="b"
                if(score(b)>high_score):
                    ans=(i,j)
                    high_score=score(b)
                b[i][j]=" "
    return ans






def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])







def is_win(board):
    for y in range(len(board)):
        for x in range(len(board)-4):
            if(board[y][x]==board[y][x+1]==board[y][x+2]==board[y][x+3]==board[y][x+4]):
                if(board[y][x]=="b"):
                    return "Black won"
                if(board[y][x]=="w"):
                    return "White won"


    for x in range(len(board)):
        for y in range(len(board)-4):
            if(board[y][x]==board[y+1][x]==board[y+2][x]==board[y+3][x]==board[y+4][x]):
                if(board[y][x]=="b"):
                    return "Black won"
                if(board[y][x]=="w"):
                    return "White won"


    for x in range (len(board)):
        for y in range(len(board)):
            if(loc_exists(board,x+4,y+4,"w")):
                if(board[y][x]==board[y+1][x+1]==board[y+2][x+2]==board[y+3][x+3]==board[y+4][x+4]):
                    return "White won"
            if(x==4 and y==3):
                print("YAY")
            if(loc_exists(board,x-4,y+4,"w")):
                print ("$$$")
                if(board[y][x]==board[y+1][x-1]==board[y+2][x-2]==board[y+3][x-3]==board[y+4][x-4]):
                    print ("$$$")
                    return "White won"







            if(loc_exists(board,x+4,y+4,"b")):
                if(board[y][x]==board[y+1][x+1]==board[y+2][x+2]==board[y+3][x+3]==board[y+4][x+4]):
                    return "Black won"

            if(loc_exists(board,x-4,y+4,"b")):
                if(board[y][x]==board[y+1][x-1]==board[y+2][x-2]==board[y+3][x-3]==board[y+4][x-4]):
                    return "Black won"


    count=0
    for i in board:
        for j in i:
            if(j==" "):
                count+=1
    if(count==0):
        return "Draw"

    return "Continue playing"








def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)







def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board








def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))







def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        game_res = is_win(board)
        print(game_res)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x







def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")






def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")







def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")






def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")






def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")






def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()






def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    play_gomoku(8)
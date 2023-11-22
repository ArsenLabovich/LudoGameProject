"""
    Start date 15.11.2023

    Introduction.

    Version 1.0 from 18.11.2023

    Project owner is Arsen Labovich API-6 FEI STU.

    By Technical Specifications project was implemented in form of Game for 2-4 players.
    Project is written in 1 file, because of Rules that OOP is banned for this project.

    List if implemented logics by Technical Specifications:

        1) n-size board drawing

        2) movement of pieces

        3) simulation of game

    Additional logics and changes in Technical Specifications:

        1) Rules was a little bit changed to implement more function and to upgrade project in possible way:

            Changes in rules:

                1) count of players 2-4 ( instead of 2)

                2) Finish is additional cell at the opposite side of board for each player

                3) Added collisions with players of different teams and for allied pieces ( if count of players is more than 2 )

                4) At the start pieces are hidden until score is less than 6

                5) When pieces reaches Finish cell it disappears and counter is decreased by 1.

        2) Implemented collisions logic for allies  and enemies:

            Allied piece can't move to cell which is occupied by other allied piece.
            Each piece can knock down opponent's piece, it means that if your piece took the place where was standing enemy's piece
            you knock down it and occupy cell. Enemy's piece returns back to it's 'home' . It means that enemy's piece hide back until player scored 6.

        3) Finish cell changes:

            In original version finish is a cell on way on cross.
            Because of console project , I can't overlay two characters on 1 cell , because of array structure and console structure.
            ( If I'll tell truth, I can, but such interface will be eye-broking, and for console project it'll more comfortable and convenient
            to make Finish-cell separated from way cells)
            So Finish for each player is 'F' cell on the opposite side of gaming field.


    GitHub Link:

        https://github.com/ArsenLabovich/LudoGamePRoject


    22.11.2023

    update

    Added displaying finished_pieces in the center of the board
    Finished pieces takes '#' cells in the direction of their start

    update

    Added skipping rule.
    If player 2 times in row scores 6, then player skips his turn.


    BugFix #1

    Fixed bug with moving piece to finish after one piece has finished

    BugFix #2

    Fixed bug in skipping turn algorithm

    update

    Added statistics in the end of the game

    update

    Added second chance after scoring 6 first time, and reworked logic of two times 6 in row.
    So now you can roll dice again after first time scoring 6 , and after 3 times scoring 6 in row you skip your turn




    If you find bug during testing my project please contact me on one of mails below:
        arsenstudcz@gmail.com
        xlabovich@stuba.sk
        xlabovich@is.stuba.sk


"""

import random
import sys
import copy

''' 
    random module to generate random numbers 
    system module to exit from program in case of wrong input data
    copy module to get deepcopy of different data structures,
    because of reference types of objects ( they keep links to objects in memory instead of keeping objects ).
'''

'''                                  '''
'''     BLOCK OF MAIN FUNCTIONS      '''
'''                                  '''


def init_game():
    print_rules()

    global board_size
    board_size = int(input("Enter board size ( odd integer more than 3) : "))

    '''
        This variable keeps board size depends on input data.
    '''

    global board
    board = []

    '''
         Variable board is our board it contains:
         '*' symbols. Those symbols is like cells where players move their pieces,
         '#' symbols. Those symbols is border of playing field,
         ' ' symbols. Those symbols is void cells, there are nothing on this cells,
         'X' symbol. This symbol is the middle of the field,
         'A' , 'B' , 'C', 'D' symbols. Those symbols is pieces of different players respectively.
         
         Then it generates initial board without any player pieces and prints it.
    '''

    global players_count
    players_count = int(input("Enter count of players (minimum count is 2 and maximum count is 4) : "))

    ''' 
        This variable keeps players count depends on input data.
    '''

    check_input_values()

    '''
        This function check all input variables and detects wrong parameters.
        In case of wrong parameters program end.
    '''

    global start_cords
    start_cords = [[board_size - 1, board_size // 2 - 1], [0, board_size // 2 + 1],
                   [board_size // 2 - 1, 0], [board_size // 2 + 1,
                                              board_size - 1], ]

    '''
        This variable keeps start cords for each player.
        Every player has n-count of pieces and every piece on the start
        Coordinates for each player in form:
        [bottom_side, top_side, left_side, right_side]  each side cords : [row, column]
        cords order : 1) Player A , 2) Player B ,` 3) Player C , 4) Player D .
    
    '''

    global finish_cords
    finish_cords = [[0, board_size // 2 + 2], [board_size - 1, board_size // 2 - 2], [board_size // 2 + 2,
                                                                                      board_size - 1],
                    [board_size // 2 - 2, 0]]

    '''
        Finish coordinates for each player in order:
        Finish cords for A, Finish cords for B,Finish cords for C,Finish cords for D.
    '''

    global players
    players = []
    fill_players()
    print_players()

    '''
        Arrays that consist of character : 
        'A' , 'B' 
        and additional characters: 'C' , 'D', in case of count of player is more than 2.
        
        function fill_players() fills array.
        function print_players() prints Letters of all Players.
    '''

    global start_pieces_count
    start_pieces_count = int((board_size - 3) / 2)

    ''' 
        Start pieces count is start count of pieces for each player,
        formula for each pieces is (n-3)/2 where n is size of board.
    '''

    global pieces_to_end_game
    pieces_to_end_game = []
    fill_pieces_to_end_game()

    ''' 
        This variable is array which keeps count of pieces to end game for each player.
        Order is Player A, Player B, Player C, Player D . 
        
        fill_pieces_to_end_game() fills array witch start_pieces_count ,
        because at the start of the game everybody should bring all pieces to the finish.
    '''

    global counts_of_escaped_pieces
    counts_of_escaped_pieces = []
    fill_counts_of_escaped_pieces()

    '''
        This variable keeps pieces that  aren't in 'their house' (which are on board).
    '''

    global player_turn
    player_turn = 1

    '''
        This variable will keep index of player which is making turn.
        Player A -> 1 player B -> 2 player C -> 3 player D -> 4 .
        After player_turn reaches value more than 4 it resets back to 1.
    '''

    global pieces_cords
    pieces_cords = {}
    set_up_start_pieces_cords()

    ''' 
        HashMap for convenient access to each  piece of each player  
        player --> list of pieces cords    example "A" --> [ [0,0], [1,1] ].
        
        set_up_start_pieces_cords() set up for each player for each piece coordinates [-1,-1].
        It means that pieces are in 'their house' . 
    '''

    global last_score_was_6
    last_score_was_6 = []
    fill_last_score_was_6()

    '''
        update 
        
        This variable keeps booleans for each player, booleans inside array shows if player's last score was 6.
    
    '''

    global statistics
    statistics = {}
    global statistic_names
    statistic_names = ["rolls count", "pieces broke", "pieces escaped", "pieces finished", "6 score on dice "]
    fill_statistics()
    print(statistics)

    generate_board(board_size)
    print_board(render_board())
    print_definitions()


def start_game():
    input("Press enter to start the game")

    '''
        This function is a little separation between initialization and game life cycle.
    '''


def game():
    while not check_is_Finished():
        print_players_turn()
        print_pieces_left()
        print_board(render_board())
        input("Press Enter to roll the dice")

        score = int(input())  # change to = int(input()) to test with different scores
        generate_number()
        print_score(score)
        if check_score(score):
            print_skipping()
            next_player_turn()
            continue
        possible_turns = generate_possible_turns(score)
        print_turns(possible_turns)
        if score == 6:
            print_second_chance()
            continue
        next_player_turn()

    '''
        It is the main function , this function is life cycle of the game.
        Player roll dice, chose from possible turns and play.
    '''


def end_game():
    winner = find_winner()
    print(f"player {winner} won the game\n")
    print_statistics()
    input(f"Press Enter to Exit\n\n")
    sys.exit(0)

    '''
        Ending game function, prints winner.
    '''


'''                                             '''
'''     BLOCK OF CHECK AND BOOLEAN FUNCTIONS    '''
'''                                             '''


def check_if_could_escape_more_pieces() -> bool:
    return start_pieces_count != count_of_escaped_pieces() and check_if_start_point_is_free()

    '''
        Function checks if player can escape more pieces on the board .
    '''


def check_is_Finished() -> bool:
    for i in pieces_to_end_game:
        if i == 0:
            return True
    return False

    '''
        Game continue till it's not finished functions checks if one of players has no pieces_to_end_game.
    '''


def check_score(score: int) -> bool:
    if score == 6:
        statistics[players[player_turn - 1]][statistic_names[4]] += 1
        if last_score_was_6[player_turn - 1] == 2:
            last_score_was_6[player_turn - 1] = 0
            return True
        else:
            last_score_was_6[player_turn - 1] += 1
    else:
        last_score_was_6[player_turn - 1] = 0
    return False

    '''
        Version 1.2 update
        
        This function checks and controls if player score 6 two times in row.
        In such case it skips turn for player.
    '''


def check_if_start_point_is_free() -> bool:
    rendered_board_cell = render_board()[start_cords[player_turn - 1][0]][start_cords[player_turn - 1][1]]
    return rendered_board_cell == "*" or rendered_board_cell != players[player_turn - 1]

    '''
        Function checks if start point to for player is free.
        It means that while exit from 'house' is not free and cell is filled with allied piece, player can not escape more pieces.
    '''


def check_input_values():
    if players_count > 4 or players_count < 2:
        print(f"Players count is incorrect , please restart the game and enter correct value.\n")
        sys.exit(0)
    if board_size % 2 == 0 or board_size < 7:
        print(f"Board size is incorrect , please restart the game and enter correct value\n")
        sys.exit(0)

    '''
        Function checks for wrong values.
        Wrong  player_count value  --->  count < 2 or  > 4 .
        Wrong  board_size   value  --->  board_size < 7 or board_size % 2 == 0 .
    '''


def check_near_cords_for_finish(cords: []) -> bool:
    finish_cords_for_player = finish_cords[player_turn - 1]
    dy = abs(finish_cords_for_player[0] - cords[0])
    dx = abs(finish_cords_for_player[1] - cords[1])
    return dx + dy == 1

    '''
        Function checking if Finish is near.
        Algorithm of working is that function count distance between Finish point and Current point,
        then if distance more than 1 we are not near Finish.
    '''


def count_of_escaped_pieces() -> int:
    counter = 0
    for cords in pieces_cords[players[player_turn - 1]]:
        if cords[0] != -1 and cords[1] != -1:
            counter += 1
    return counter

    '''
        This function returns count of escaped pieces of current turn player.
    '''


def is_Left_side(cords: []) -> bool:
    return cords[1] <= board_size // 2

    ''' 
        Function determines side of piece.
        Used in way Finding function.
    '''


def is_Top_side(cords: []) -> bool:
    return cords[0] <= board_size // 2

    ''' 
        Function determines side of piece.
        Used in way Finding function.
    '''


def is_Bottom_side(cords: []) -> bool:
    return cords[0] > board_size // 2

    ''' 
        Function determines side of piece.
        Used in way Finding function.
    '''


def is_equal_cords(cords1: [], cords2: []) -> bool:
    return cords1[0] == cords2[0] and cords1[1] == cords2[1]

    '''
        Function which determine if cords equals.
        Comparing one by one because of reference types.
        We can't compare arrays using == ( i'm not sure in python , byt in c++ and java sure you can't use that).
        We should compare values , not links, links of course will be  different.
    '''


'''                                         '''
'''     BLOCK OF INITIALIZATION FUNCTIONS   '''
'''                                         '''


def set_up_start_pieces_cords():
    for i in range(0, players_count):
        pieces_cords_list = []
        for _ in range(start_pieces_count):
            cords = [-1, -1]
            pieces_cords_list.append(cords)
        pieces_cords[players[i]] = pieces_cords_list

    ''' 
        On the start of the game each piece is in imagined 'house'
        and it will escape 'house' only when player rolls a 6 on the dice,
        then piece escape and got to the its start cords
        start cords for each piece are [-1,-1].
    '''


def generate_board(n: int):
    global players_count
    center = n // 2
    for y in range(n):
        row = []

        for x in range(n):
            if (x < center - 1 or x > center + 1) and (y < center - 1 or y > center + 1):
                row.append(" ")
                continue
            elif y == center or x == center:
                if x == y == center:
                    row.append("X")
                elif (x == 0 or x == (n - 1)) or (y == 0 or y == (n - 1)):
                    row.append("*")
                else:
                    row.append("#")
            elif (x == (center - 1) or x == (center + 1)) or (y == (center - 1) or y == (center + 1)):
                row.append("*")
            else:
                row.append(" ")
        board.append(row)
    for i in range(0, players_count):
        board[finish_cords[i][0]][finish_cords[i][1]] = "F"

    '''
        Function generates pattern of n-size x-finishes pattern of board.
        This pattern is used to render and print board.
    '''


def fill_players():
    for i in range(0, players_count):
        players.append(chr(i + 65))

    '''
        Fills players array with 'A' ,'B' , 'C', 'D' depends on count of players.
    '''


def fill_pieces_to_end_game():
    for _ in range(players_count):
        pieces_to_end_game.append(start_pieces_count)

    '''
        Setting up for all players start count of pieces_to_end_game.
        Depends on formula of counting start count of pieces (board_size - 3 / 2).
    '''


def fill_last_score_was_6():
    for i in range(players_count):
        last_score_was_6.append(0)

    '''
        Filling start variable, at the start nobody has scored 6.
    '''


def fill_counts_of_escaped_pieces():
    for _ in range(players_count):
        counts_of_escaped_pieces.append(0)

    '''
        Setting up for all players start count of escaped pieces.
        At the start all players bring zero pieces to the Finish.
    '''


def fill_statistics():
    global statistics

    for player_index in range(0, players_count):
        player_key = players[player_index]
        statistics[player_key] = {}
        for statistic_name in statistic_names:
            statistics[player_key][statistic_name] = 0


'''                                    '''
'''        BLOCK OF PRINT FUNCTIONS     '''
'''                                    '''


def print_rules():
    print(f" \n\n\n"
          f" Mensch ärgere Dich nicht \n\n\n"
          f" Rules: \n"
          f" There is a board, each player starts from it's own side of board.\n"
          f" For A player it's bottom side, for B player it's top side, for C player it's left side and for D player it's right side.\n"
          f" Each player has n-count of pieces, it depends ot size of the board.\n"
          f" You can chose count of players ( between 2 and 4 ) and  size of board ( recommended to use at least 7nd size , required condition that size should be odd).\n"
          f" To win player should bring all pieces to the Finish.\n"
          f" Each player has it's own Finish, for each player Finish is situated on the other side of the Start cell.\n"
          f" For example A player starts from bottom side, so A player should bring all pieces to the Top side.\n"
          f" At the start of the game all pieces are 'hidden'. You should roll 6 on the dice to get out on the board one of your pieces.\n"
          f" If you have no pieces on the board you can move anything, so until you first roll 6 you can move anything :).\n"
          f" When in game more than 2 players appears collisions, it means that A piece can take the same place with C piece and other pieces too.\n"
          f" In case of collision piece that was staying ( not moving ) return back to it's home.\n"
          f" For example, A player is moving it's piece, and at the end of his move his piece took the same cell with C piece.\n"
          f" In that case C piece will return to it's home( home means that piece become hidden )."
          f"\n\n\n")


def print_statistics():
    for player_key in statistics.keys():
        print(f"Statistics for {player_key} player:\n\n")
        for statistics_name in statistics[player_key].keys():
            print(f"    {statistics_name} - {statistics[player_key][statistics_name]}\n")


def print_definitions():
    print(f" \n\n\n"
          f" Definitions:\n"
          f" symbols A,B,C,D are pieces of players respectively.\n"
          f" symbols * are cells where pieces could move.\n"
          f" symbols # are borders between cells.\n"
          f" symbols F are Finishes for different players , in the rules where described where Finish for each player."
          f"\n\n\n")


def print_second_chance():
    print(f"Player {players[player_turn - 1]} scored 6, so he can roll the dice again and make turn again")


def print_pieces_left():
    print(f"Pieces to end game:  {pieces_to_end_game[player_turn - 1]}\n")


def print_players():
    print(f"Players : ")
    for player in players:
        print(f"{player} ", end="")
    print(f" are playing.\n\n\n")


def print_score(score: int):
    print(f"Player {(players[player_turn - 1])} scored {str(score)}.\n\n")


def print_players_turn():
    print(f"Player {players[player_turn - 1]}'s turn.\n\n")


def print_turns(possible_turns: {}):
    if len(possible_turns) == 0:
        print(
            f"You have no pieces on a board and you rolled less than six," +
            f" it means that you can't escape and move your pieces.\n\n")
    else:
        print(f"Make your turn: \n\n")
        for key, value in possible_turns.items():
            print(f"{key}")
        selected_turn = int(input())
        make_turn(possible_turns, selected_turn)


def print_skipping():
    print(f"You scored 6 3 times in row, so you are cheater and you skip turn")
    print(f"Player {players[player_turn - 1]} skips his turn ")


def print_board(rendered_board: []):
    for row in rendered_board:
        for element in row:
            print(f"{element}  ", end="")
        print(f"\n")
    print(f"\n\n")


def print_collision(alive_piece_key: str, destroyed_piece_key: str):
    print(
        f" Player {alive_piece_key} destroyed {destroyed_piece_key}'s piece, so {destroyed_piece_key} piece returns back to home until it'll escape)")


'''                                 '''
'''     BLOCK OF ACTION FUNCTIONS   '''
'''                                 '''


def destroy_collision(player_key: str, cords: []):
    for key in pieces_cords.keys():
        if key != player_key:
            for i in range(0, len(pieces_cords[key])):
                temp_cords = pieces_cords[key][i]
                if temp_cords[0] == cords[0] and temp_cords[1] == cords[1]:
                    pieces_cords[key][i] = [-1, -1]
                    print_collision(player_key, key)

    '''
        This function destroys collision.
        It means that this function return figure that was before on current cell back to home.
    '''


def next_player_turn():
    global player_turn
    player_turn += 1
    if player_turn > players_count:
        player_turn = 1

    '''
        This Functions switches turn.
        In this cycle  1 -> 2 -> 3 -> 4 .
    '''


def render_board() -> [[]]:
    rendered_board = copy.deepcopy(board)

    dx_dy_for_rendering_finished_pieces = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    for player in pieces_cords.keys():
        for cords in pieces_cords[player]:
            if cords != [-1, -1] and cords not in finish_cords:
                rendered_board[cords[0]][cords[1]] = str(player)

    for player_key in pieces_cords.keys():
        dy = dx_dy_for_rendering_finished_pieces[players.index(player_key)][1]
        dx = dx_dy_for_rendering_finished_pieces[players.index(player_key)][0]
        start_render_cords = [board_size // 2 + dy, board_size // 2 + dx]
        for cords in pieces_cords[player_key]:
            if cords in finish_cords:
                rendered_board[start_render_cords[0]][start_render_cords[1]] = player_key
                start_render_cords[0] += dy
                start_render_cords[1] += dx

    return rendered_board

    '''
        Function renders board and fill board with pieces.
        After each turn border re-renders and pieces moves to another coordinates.
        
        Version 1.1 update:
        
        Function update:
        Now after finishing  pieces are displaying in the center of the board instead of
        '#' cell, instead of hiding after finishing.
    '''


def generate_number() -> int:
    statistics[players[player_turn - 1]][statistic_names[0]] += 1
    return random.randint(1, 6)

    '''
        Function generates random number.
    '''


def make_turn(possible_turns: {}, number_of_turn: int):
    global pieces_to_end_game
    key = list(possible_turns.keys())[number_of_turn - 1]
    player_key = players[player_turn - 1]
    cords_array = possible_turns[key]
    cords_of_pieces = pieces_cords[player_key]
    old_cords = cords_array[0]
    new_cords = cords_array[1]
    for i in range(0, len(cords_of_pieces)):
        current_cords = cords_of_pieces[i]
        if is_equal_cords(current_cords, old_cords):
            cords_of_pieces[i] = new_cords
            pieces_cords[players[player_turn - 1]] = copy.deepcopy(cords_of_pieces)
            if new_cords in finish_cords:
                pieces_to_end_game[player_turn - 1] -= 1
                statistics[players[player_turn - 1]][statistic_names[3]] += 1
            else:
                destroy_collision(player_key, new_cords)
            if new_cords in start_cords:
                statistics[players[player_turn - 1]][statistic_names[2]] += 1
            elif new_cords in finish_cords:
                statistics[players[player_turn - 1]][statistic_names[3]] += 1
            return

    '''
        Function detects player chose and apply changes to game.
    '''


def generate_possible_turns(
        score: int) -> {}:
    possible_turns = {}
    number_of_turn = 1

    if score == 6:
        if check_if_could_escape_more_pieces():
            current_cords = [-1, -1]
            new_cords = start_cords[player_turn - 1]
            possible_turn = [current_cords, new_cords]
            possible_turns[f"{number_of_turn}) Release 1 more piece on board"] = possible_turn
            number_of_turn += 1
    for cords in pieces_cords[players[player_turn - 1]]:
        if cords != [-1, -1] and cords not in finish_cords:
            current_cords = cords
            new_cords = generate_next_cords(score, current_cords)
            if new_cords in pieces_cords[players[player_turn - 1]]:
                if new_cords not in finish_cords:
                    continue
            possible_turn = [current_cords, new_cords]
            if new_cords == finish_cords[player_turn - 1]:
                possible_turn_description = (
                    f" {str(number_of_turn)}) Move piece on coordinates {str(current_cords)} to Finish")
            else:
                possible_turn_description = (
                    f"{str(number_of_turn)}) Move piece on coordinates  {str(current_cords)} on {str(score)} cells forward ")
            number_of_turn += 1
            possible_turns[possible_turn_description] = possible_turn
    return possible_turns

    '''
        This function generates all possible next moves
        It could be:
        1) escape piece
        2) put piece on finish
        3) put piece on x cells forward
    '''


def generate_next_cords(score: int,
                        cords: []) -> []:
    if check_near_cords_for_finish(cords):
        return finish_cords[player_turn - 1]
    if is_Left_side(cords):

        # left side of field

        if is_Bottom_side(cords):

            # left bottom part of field

            if (ord(board[cords[0] - 1][cords[1]]) == 42) or (65 <= ord(board[cords[0] - 1][cords[1]]) <= 69):
                if score == 1:
                    return [cords[0] - 1, cords[1]]
                else:
                    return generate_next_cords(score - 1, [cords[0] - 1, cords[1]])

            # coordinates for top cell

            elif cords[1] - 1 >= 0 and (
                    (ord(board[cords[0]][cords[1] - 1]) == 42) or (65 <= ord(board[cords[0]][cords[1] - 1]) <= 69)):
                if score == 1:
                    return [cords[0], cords[1] - 1]
                else:
                    return generate_next_cords(score - 1, [cords[0], cords[1] - 1])

            # coordinates for left cell

        elif is_Top_side(cords):

            # left top part of field

            if cords[0] - 1 >= 0 and (
                    (ord(board[cords[0] - 1][cords[1]]) == 42) or (65 <= ord(board[cords[0] - 1][cords[1]]) <= 69)):
                if score == 1:
                    return [cords[0] - 1, cords[1]]
                else:
                    return generate_next_cords(score - 1, [cords[0] - 1, cords[1]])

            # coordinates for top cell

            else:
                if (ord(board[cords[0]][cords[1] + 1]) == 42) or (65 <= ord(board[cords[0]][cords[1] + 1]) <= 69):
                    if score == 1:
                        return [cords[0], cords[1] + 1]
                    else:
                        return generate_next_cords(score - 1, [cords[0], cords[1] + 1])

            # coordinates for right cell
    else:

        # right side of field

        if is_Top_side(cords):

            # right top part of field

            if (ord(board[cords[0] + 1][cords[1]]) == 42) or (65 <= ord(board[cords[0] + 1][cords[1]]) <= 69):
                if score == 1:
                    return [cords[0] + 1, cords[1]]
                else:
                    return generate_next_cords(score - 1, [cords[0] + 1, cords[1]])

                # coordinates for bottom

            elif (cords[1] + 1) < board_size and (ord(board[cords[0]][cords[1] + 1]) == 42) or (
                    65 <= ord(board[cords[0]][cords[1] + 1]) <= 69):
                if score == 1:
                    return [cords[0], cords[1] + 1]
                else:
                    return generate_next_cords(score - 1, [cords[0], cords[1] + 1])

                # coordinates for right cell

        elif is_Bottom_side(cords):

            # right bottom part of field

            if cords[0] + 1 < board_size and (
                    (ord(board[cords[0] + 1][cords[1]]) == 42) or (65 <= ord(board[cords[0] + 1][cords[1]]) <= 69)):
                if score == 1:
                    return [cords[0] + 1, cords[1]]
                else:
                    return generate_next_cords(score - 1, [cords[0] + 1, cords[1]])

                # coordinates for bottom cell
            elif (ord(board[cords[0]][cords[1] - 1]) == 42) or (65 <= ord(board[cords[0]][cords[1] - 1]) <= 69):
                if score == 1:
                    return [cords[0], cords[1] - 1]
                else:
                    return generate_next_cords(score - 1, [cords[0], cords[1] - 1])

            # coordinates for left cell

    '''
        This is big recursive works wayFinder Algorithm.
        How it works?
        We have 4 parts of gaming field. 4 Corners.
        In each corner we can move only in 2 directions,
        And each cell has only one next cell.
        So function determine part of field, and depends on that determine 1 cell in two directions.
        Then function recursively calls the same function , but with cords cell that we find, and decrease cells that we should find by 1.
        If we should find 1 cell, so next cords are cords that we are searching.    
    '''


def find_winner() -> str:
    for i in range(len(pieces_to_end_game)):
        if pieces_to_end_game[i] == 0:
            return players[i]

    '''
        This function finds winner.
        Winner is first player with zero pieces_to_end_game.
    '''


'''                         '''
'''     END OF FUNCTIONS    '''
'''                         '''

init_game()
start_game()
game()
end_game()

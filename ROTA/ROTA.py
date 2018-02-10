import requests
import logging
import base64
import time






class Server(object):
    url = 'https://rota.praetorian.com/rota/service/play.php'
    log = logging.getLogger(__name__)

    def __init__(self):
        self.session = requests.Session()

    def _request(self, route):
        while True:
            try:
                r = self.session.get(self.url + route)
                if r.status_code == 429:
                    raise Exception('Rate Limit Exception')
                if r.status_code == 500:
                    raise Exception('Unknown Server Exception')
                return r.json()
            except Exception as e:
                self.log.error(e)
                self.log.info('Waiting 60 seconds before next request')
                time.sleep(60)

    def initialize(self):
        return self._request("?request=new&email=mattchamberlain2@gmail.com")

    def place(self, x):
        return self._request("?request=place&location=" + str(x))

    def move(self, x, y):
        return self._request("?request=move&from=" + str(x) + "&to=" + str(y))

    def status(self):
        return self._request("?request=status")

    def next(self):
        return self._request("?request=next")

class Board(object):
    s = Server()
    board_state = "---------"
    player_wins = 0
    computer_wins = 0
    moves = 0
    games_won = 0
    hash = ""

    game_active = False
    current_game_str = []
    def __init__(self):
        self.handle_json(self.s.initialize())

    def handle_json(self, r):
        if r.get('status', '') != 'success':
            print('Request failed')
            print(r)
            raise Exception('Failed Request')
        else:
            self.read_data(r.get('data', []))

    def read_data(self, data):
        if self.games_won >= 50:
            self.hash = data['hash']
            print('Success!')
            print(self.hash)
            exit(0)
            return
        try:
            self.board_state = data['board']
        except:
            self.hash = data['hash']
            print("Hash: " + str(self.hash))
            print("No new board state, could be because of winning the challenge or some other bug.")
            exit(1)
        self.player_wins = data['player_wins']
        self.computer_wins = data['computer_wins']
        self.moves = data['moves']
        self.games_won = data['games_won']

        if self.moves > 30:
            self.next()
            self.game_active = False



        if self.computer_wins > 0:
            print('Failure!')
            for s in self.current_game_str:
                print(s)
            print(self)
            print(data)
            exit(1)

    def place(self, x):
        self.handle_json(self.s.place(x))

    def move(self, x, y):
        self.handle_json(self.s.move(x, y))

    def status(self):
        self.handle_json(self.s.status())

    def next(self):
        self.handle_json(self.s.next())

    def clockwise(self, location):
        if location < 1:
            print("Invalid location")
            exit(1)
        if location == 1:
            return 2
        if location == 2:
            return 3
        if location == 3:
            return 6
        if location == 4:
            return 1
        if location == 5:
            print("Clockwise in middle")
            return 5
        if location == 6:
            return 9
        if location == 7:
            return 4
        if location == 8:
            return 7
        if location == 9:
            return 8

    def counter_clockwise(self, location):
        if location < 1:
            print("Invalid location")
            exit(1)
        if location == 1:
            return 4
        if location == 2:
            return 1
        if location == 3:
            return 2
        if location == 4:
            return 7
        if location == 5:
            print("Counter-Clockwise in middle")
            return 5
        if location == 6:
            return 3
        if location == 7:
            return 8
        if location == 8:
            return 9
        if location == 9:
            return 6

    def can_move(self, loc):
        return self.board_state[loc - 1] == '-'

    def win_cross(self, char, move):
        if self.board_state[5 - 1] != char and move[1] != 5:
            return False
        if move[0] == 5:
            return False
        indices = [(i+1) for i, c in enumerate(self.board_state) if c == char]
        if move[0] != 0:
            indices.remove(move[0])
        indices.append(move[1])
        return sum(indices) == 15

    def win_edge(self, char, move):
        locs = [(i + 1) for i, c in enumerate(self.board_state) if c == char]
        if move[0] != 0:
            locs.remove(move[0])
        locs.append(move[1])
        if 5 in locs:
            return False
        for loc in locs:
            cw = self.clockwise(loc)
            ccw = self.counter_clockwise(loc)
            if (cw in locs) and (self.clockwise(cw) in locs):
                return True
            if (ccw in locs) and (self.counter_clockwise(ccw) in locs):
                return True
        return False

    def check_place_win(self, char):
        for loc in range(1, 10):
            if not self.can_move(loc):
                continue
            if self.win_cross(char, (0, loc)):
                return loc
            if self.win_edge(char, (0, loc)):
                return loc
        return 0

    def opening_moves(self):
        self.game_active = True

        # print(self)
        self.current_game_str.append(str(self))
        # First place is either bottom of the board or counter clockwise to a computer piece
        if 'c' in self.board_state:
            loc = self.board_state.index('c') + 1
            if loc == 5:
                self.place(8)
            else:
                self.place(self.counter_clockwise(loc))
        else:
            self.place(8)
        # print(self)
        self.current_game_str.append(str(self))
        # Second place makes sure the computer cannot win with their next move
        # Otherwise attempts to box in one of the computer pieces on the outside
        loc = self.check_place_win('c')
        if loc == 0:
            for i in range(1, 10):
                if self.board_state[i-1] == 'c':
                    if i == 5:
                        loc = 10 - (self.board_state.index('p') + 1)
                        self.place(loc)
                        break
                    cw = self.clockwise(i)
                    ccw = self.counter_clockwise(i)
                    if self.can_move(cw) and not self.near_piece('p', 0, cw):
                        self.place(cw)
                        break
                    if self.can_move(ccw) and not self.near_piece('p', 0, ccw):
                        self.place(ccw)
                        break
        else:
            self.place(loc)
        # print(self)
        self.current_game_str.append(str(self))

        # Third place makes sure the computer cannot win with their next move
        # Otherwise it plays clockwise where it can from a computer piece as long as its not near a friendly piece
        loc = 0
        if self.board_state.count('c') == 2:
            loc = self.check_place_win('c')
        else:
            their_winning_moves = self.winning_moves('c')
            their_possible_moves = self.find_moves('c')
            for possible_move in their_possible_moves:
                if (possible_move in their_winning_moves):
                    loc = possible_move[1]
                    if self.can_move(loc):
                        continue
        # print(loc)
        if loc == 0:
            prev = self.board_state.index('c') + 1
            while True:
                if prev == 5:
                    prev = 8
                cw = self.clockwise(prev)
                if self.can_move(cw) and not self.near_piece('p', 0, cw):
                    self.place(cw)
                    break
                prev = cw
        else:
            self.place(loc)

        # print(self)
        self.current_game_str.append(str(self))
        if self.board_state.count('c') != 3:
            raise Exception("Not enough pieces placed")
    # finds all possible moves and returns them as a tuple of (current, possible)
    def find_moves(self, char):
        moves = []
        locs = [(i + 1) for i, c in enumerate(self.board_state) if c == char]
        for loc in locs:
            if loc == 5:
                for i in range(1, 10):
                    if i == 5:
                        continue
                    if self.can_move(i):
                        moves.append((loc, i))

            else:
                cw = self.clockwise(loc)
                ccw = self.counter_clockwise(loc)
                middle = 5
                if self.can_move(cw):
                    moves.append((loc, cw))
                if self.can_move(ccw):
                    moves.append((loc, ccw))
                if self.can_move(middle):
                    moves.append((loc, middle))

        return moves

    # finds all moves (even if currently blocked) that can win the game
    # returns them as a tuple of (current, possible)
    def winning_moves(self, char):
        moves = []
        locs = [(i + 1) for i, c in enumerate(self.board_state) if c == char]
        for loc in locs:
            if loc == 5:
                for i in range(1, 10):
                    if i == 5:
                        continue
                    if self.win_cross(char, (loc, i)) or self.win_edge(char, (loc, i)):
                        moves.append((loc, i))

            else:
                cw = self.clockwise(loc)
                ccw = self.counter_clockwise(loc)
                middle = 5
                if self.win_cross(char, (loc, cw)) or self.win_edge(char, (loc, cw)):
                    moves.append((loc, cw))
                if self.win_cross(char, (loc, ccw)) or self.win_edge(char, (loc, ccw)):
                    moves.append((loc, ccw))
                if self.win_cross(char, (loc, middle)) or self.win_edge(char, (loc, middle)):
                    moves.append((loc, middle))

        return moves
    def near_piece(self, char, current_loc, loc):
        if loc == 5:
            return True
        cw = self.clockwise(loc)
        ccw = self.counter_clockwise(loc)

        if cw == current_loc:
            return self.board_state[ccw - 1] == char
        if ccw == current_loc:
            return self.board_state[cw - 1] == char
        return (self.board_state[cw - 1] == char) or (self.board_state[ccw - 1] == char)


    def defense(self):
        # print(self)
        self.current_game_str.append(str(self))

        our_moves = self.find_moves('p')
        their_moves = self.winning_moves('c')
        # Check if we can win the game
        for move in our_moves:
            if self.win_edge('p', move) or self.win_cross('p', move):
                print("We won the game!")
                print(self)
                self.move(move[0], move[1])
                print(self)
                return





        # prune the possible moves for both teams
        our_locs = [(i + 1) for i, c in enumerate(self.board_state) if c == 'p']
        # make a copy of lists so we can remove values from the real one within the loop
        for their_move in their_moves[:]:
            # if we already have a piece there, we don't want to move the piece
            if their_move[1] in our_locs:
                their_moves.remove(their_move)
                for our_move in our_moves[:]:
                    if our_move[0] == their_move[1]:
                        our_moves.remove(our_move)


        # print("Theirs:")
        # print(their_moves)

        # print("Ours:")
        # print(our_moves)

        comp_win_locs = []
        # Create list of all possible win locations
        for move in their_moves:
            comp_win_locs.append(move[1])

        comp_win_locs = list(set(comp_win_locs))
        # print(comp_win_locs)

        if len(comp_win_locs) > 1:
            print("Computer guaranteed win")
            print(self)
            exit(1)

        # If there is only one location, we need to find it and move there with a valid piece
        if comp_win_locs:
            for move in our_moves:
                if move[1] == comp_win_locs[0]:
                        self.move(move[0], move[1])
                        # print(self)
                        return

        # If there is no way for the computer to win, we need to first, try to leave the middle
        # Second we pick a random movement always staying away from friendly pieces
        else:
            for move in our_moves:
                if move[0] == 5:
                    # check valid locations away from friendly pieces
                    for i in range(1, 10):
                        if i == 5:
                            continue
                        if not self.near_piece('p', move[0], i) and (move[1] == i):
                            self.move(move[0], move[1])
                            # print(self)
                            return


            for move in our_moves:
                    if move[1] == 5:
                        continue
                    if not self.near_piece('p', move[0], move[1]):
                        self.move(move[0], move[1])
                        # print(self)
                        return

        print("Could not move intelligently, most likely because we were forced into the center")
        print(self)
        exit(1)

    def __str__(self):
        to_return = ''
        for i in range(len(self.board_state)):
            to_return += self.board_state[i]
            if not (i+1) % 3:
                to_return += '\n'
        return to_return




b = Board()


# We are using a very defensive algorithm
while b.games_won <= 50:
    b.current_game_str = []
    print("Total games: " + str(b.games_won)
          + " Computer wins: " + str(b.computer_wins)
          + " Player wins: " + str(b.player_wins))
    b.opening_moves()
    while b.game_active:
        b.defense()
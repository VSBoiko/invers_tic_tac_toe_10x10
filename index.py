"""
Inversion Tic-Tac-Toe 10x10 game.
"""
import random
from math import inf


class TicTacToe:
    def __init__(self):
        self.players_marks = ['X', 'O']

        self.column_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        self.row_nums = [str(row_num) for row_num in range(1, 11)]
        self.board: dict = {}
        for column_char in self.column_chars:
            for row_num in self.row_nums:
                if column_char not in self.board:
                    self.board[column_char]: dict = {}
                self.board[column_char][row_num] = False

        self.player: str = ""
        self.ai: str = ""
        self.current_player_mark: str = ""
        self.game_result: str = ""
        self.last_turn: tuple = (random.choice(self.column_chars),
                                 random.choice(self.row_nums))

    def play(self):
        print('Welcome to Tic Tac Toe!')

        self.player, self.ai = self._player_input()
        self.current_player_mark = self._choose_first()

        print(f'Player with mark "{self.current_player_mark}" goes first.')

        is_game_over = False
        while not is_game_over:
            self._display_board()

            print(f'Turn of the player with the mark "{self.current_player_mark}":')

            if self.current_player_mark == self.ai:
                player_pos_char, player_pos_num = self._ai_turn()
                self._place_marker(player_pos_char, player_pos_num)
            else:
                player_pos_char, player_pos_num = self._player_choice()
                self._place_marker(player_pos_char, player_pos_num)

            self.last_turn = (player_pos_char, player_pos_num)

            if self._check_game_finish(self.board, player_pos_char, player_pos_num):
                is_game_over = True
            else:
                self.current_player_mark = self._switch_player(self.current_player_mark)
        if self.game_result == "draw":
            print('The game ended in a draw.')
        elif self.game_result in self.players_marks:
            print(f'The player with the mark "{self.game_result}" wins!')
        else:
            print("Game error!")

    def _ai_turn(self):
        current_player_mark = self.current_player_mark
        ai_board = self.board.copy()
        best_score = -inf
        n = 0
        best_turns: list = []

        pos_char, pos_num = self.last_turn
        columns, rows = self.column_chars, self.row_nums
        char_ind, num_ind = columns.index(pos_char), rows.index(pos_num)

        x_from, x_to = self._get_interval(char_ind, 2)
        y_from, y_to = self._get_interval(num_ind, 2)
        for i in range(x_from, x_to + 1):
            x = columns[i]
            column = self.board[x]
            for j in range(y_from, y_to + 1):
                y = rows[j]
                cell = column[y]
                if not cell:
                    n += 1
                    ai_board[x][y] = current_player_mark
                    score = self._minimax(ai_board, x, y, 0, True)
                    ai_board[x][y] = False
                    if best_score < score:
                        best_score = score
                        best_turns.clear()
                        best_turns.append((x, y))
                    elif best_score == score:
                        best_score = score
                        best_turns.append((x, y))
        return random.choice(best_turns)

    def _minimax(self, board, pos_char, pos_num, depth, player_turn):
        game_result = self._check_game_finish(board, pos_char, pos_num)
        if (game_result == "draw") or (depth > 2):
            return 0
        elif game_result == self.player:
            return -10
        elif game_result == self.ai:
            return 10

        columns, rows = self.column_chars, self.row_nums
        char_ind, num_ind = columns.index(pos_char), rows.index(pos_num)

        x_from, x_to = self._get_interval(char_ind, 1)
        y_from, y_to = self._get_interval(num_ind, 1)
        if player_turn:
            best_score = inf
            for i in range(x_from, x_to + 1):
                x = columns[i]
                column = board[x]
                for j in range(y_from, y_to + 1):
                    y = rows[j]
                    cell = column[y]
                    if not cell:
                        board[x][y] = self.player
                        score = self._minimax(board, pos_char, pos_num, depth + 1, False)
                        board[x][y] = False
                        best_score = min(best_score, score)
        else:
            best_score = - inf
            for x, column in board.items():
                for y, cell in column.items():
                    if not cell:
                        board[x][y] = self.ai
                        score = self._minimax(board, x, y, depth + 1, True)
                        board[x][y] = False
                        best_score = max(best_score, score)
        return best_score

    def _get_interval(self, pos, deviation):
        if int(pos) <= deviation:
            pos_from, pos_to = 0, deviation * 2
        elif int(pos) >= 9 - deviation + 1:
            pos_from, pos_to = 9 - deviation * 2, 9
        else:
            pos_from, pos_to = pos - deviation, pos + deviation

        return pos_from, pos_to

    def _display_board(self):
        """Prints the game board."""
        print(' ' * 2 + ' | ' + ' | '.join(str(char) for char in self.column_chars))
        for row_num in self.row_nums:
            self._display_row(str(row_num))

    def _display_row(self, row_num):
        """Prints the game board row."""
        row = f'{row_num}' if len(row_num) == 2 else f' {row_num}'
        for column_chars in self.column_chars:
            if not self.board[column_chars][row_num]:
                row += f' | -'
            else:
                row += f' | {self.board[column_chars][row_num]}'
        print(row)

    def _player_input(self):
        """Gets player's input string to choose the game mark to play."""
        player = ''
        while player not in self.players_marks:
            player = input('Please, choose your marker: X or O: ')

        ai = 'O' if player == 'X' else 'X'
        return player, ai

    def _place_marker(self, pos_char, pos_num):
        """Puts a player mark to appropriate position."""
        self.board[pos_char][pos_num] =  self.current_player_mark

    def _get_loss_interval(self, pos):
        pos_from = (pos - 4) if (pos - 4) >= 0 else 0
        pos_to = (pos + 4) if (pos + 4) <= 9 else 9
        return pos_from, pos_to

    def _is_loss_line(self, line):
        return ("X" * 5 in line) or ("O" * 5 in line)

    def _check_horizontal(self, board, pos_char, pos_num):
        columns, rows = self.column_chars, self.row_nums
        char_ind, num_ind = columns.index(pos_char), rows.index(pos_num)

        col_from, col_to = self._get_loss_interval(char_ind)
        horizontal = ""
        for i in range(col_from, col_to + 1):
            cell = board[columns[i]][pos_num]
            horizontal += cell if cell else "-"
        return self._is_loss_line(horizontal)

    def _check_vertical(self, board, pos_char, pos_num):
        columns, rows = self.column_chars, self.row_nums
        char_ind, num_ind = columns.index(pos_char), rows.index(pos_num)

        row_from, row_to = self._get_loss_interval(num_ind)
        vertical = ""
        for i in range(row_from, row_to + 1):
            cell = board[pos_char][rows[i]]
            vertical += cell if cell else "-"
        return self._is_loss_line(vertical)

    def _check_diagonals(self, board, pos_char, pos_num):
        columns, rows = self.column_chars, self.row_nums
        char_ind, num_ind = columns.index(pos_char), rows.index(pos_num)

        x, y = char_ind, num_ind
        diagonal = ""
        reverse_diagonal = ""
        for i in range(-4, 5):
            if 0 <= (x + i) <= 9 and 0 <= (y + i) <= 9:
                cell = board[columns[x + i]][rows[y + i]]
                diagonal += cell if cell else "-"
            if 0 <= (x + i) <= 9 and 0 <= (y - i) <= 9:
                cell = board[columns[x + i]][rows[y - i]]
                reverse_diagonal += cell if cell else "-"
        return (self._is_loss_line(diagonal) or
                self._is_loss_line(reverse_diagonal))

    def _loss_check(self, board, pos_char, pos_num):
        """Returns boolean value whether the player wins the game."""
        return (self._check_horizontal(board, pos_char, pos_num)) or \
               (self._check_vertical(board, pos_char, pos_num)) or \
               (self._check_diagonals(board, pos_char, pos_num))

    def _choose_first(self):
        """Randomly returns the player's mark that goes first."""
        return self.players_marks[random.choice((0, 1))]

    def _space_check(self, pos_char, pos_num):
        """Returns boolean value whether the cell is free or not."""
        return self.board[pos_char][pos_num] not in self.players_marks

    def _full_board_check(self, board):
        """Returns boolean value whether the game board is full of game marks."""
        for row in board.values():
            if False in set(row.values()):
                return False
        return True

    def _player_choice(self):
        """Gets player's next position and check if it's appropriate to play."""
        player_mark = self.current_player_mark
        while True:
            try:
                pos = input(f'Player "{player_mark}", your turn (for example, a10): ')
                pos_char, pos_num = pos[0], pos[1:]
                if (pos_char in self.board) and (pos_num in self.board[pos_char]) \
                        and (self._space_check(pos_char, pos_num)):
                    return pos_char, pos_num
                else:
                    raise ValueError
            except ValueError as exc:
                print(f'Wrong value: {exc}. Please, try again.')

    def _switch_player(self, player_mark):
        """Switches player's marks to play next turn."""
        return 'O' if player_mark == 'X' else 'X'

    def _check_game_finish(self, board, pos_char, pos_num):
        """Return boolean value is the game finished or not."""
        if self._loss_check(board, pos_char, pos_num):
            self.game_result = self._switch_player(self.current_player_mark)
            return True

        if self._full_board_check(board):
            self.game_result = "draw"
            return True

        return False


def replay():
    """Asks the players to play again."""
    decision = ''
    while decision not in ('y', 'n'):
        decision = input('Would you like to play again? Type "y" or "n"')

    return decision == 'y'


def clear_screen():
    """Clears the game screen via adding new rows."""
    print('\n' * 100)


tt = TicTacToe()
play_game = True
while play_game:
    tt.play()
    if replay():
        clear_screen()
        del tt
        tt = TicTacToe()
    else:
        play_game = False

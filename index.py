"""
Inversion Tic-Tac-Toe 10x10 game.
"""
import random


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

        self.player_first: str = ""
        self.player_second: str = ""
        self.current_player_mark: str = ""

    def play(self):
        print('Welcome to Tic Tac Toe!')

        self.player_first, self.player_second = self._player_input()
        self.current_player_mark = self._choose_first()

        print(f'Player with mark "{self.current_player_mark}" goes first.')

        is_game_over = False
        while not is_game_over:
            self._display_board()

            print(f'Turn of the player with the mark "{self.current_player_mark}":')

            player_pos_char, player_pos_num = self._player_choice()
            self._place_marker(player_pos_char, player_pos_num)

            if self._check_game_finish(player_pos_char, player_pos_num):
                is_game_over = True
            else:
                self.current_player_mark = self._switch_player()

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
        player_first = ''
        while player_first not in self.players_marks:
            player_first = input('Please, choose your marker: X or O: ')

        player_second = 'O' if player_first == 'X' else 'X'
        return player_first, player_second

    def _place_marker(self, pos_char, pos_num):
        """Puts a player mark to appropriate position."""
        self.board[pos_char][pos_num] = self.current_player_mark

    def _get_loss_interval(self, pos):
        pos_from = (pos - 4) if (pos - 4) >= 0 else 0
        pos_to = (pos + 4) if (pos + 4) <= 9 else 9
        return pos_from, pos_to

    def _is_loss_line(self, line):
        return ("X" * 5 in line) or ("O" * 5 in line)

    def _check_horizontal(self, pos_char, pos_num):
        board, columns, rows = self.board, self.column_chars, self.row_nums
        char_ind, num_ind = columns.index(pos_char), rows.index(pos_num)

        col_from, col_to = self._get_loss_interval(char_ind)
        horizontal = ""
        for i in range(col_from, col_to + 1):
            cell = board[columns[i]][pos_num]
            horizontal += cell if cell else "-"
        return self._is_loss_line(horizontal)

    def _check_vertical(self, pos_char, pos_num):
        board, columns, rows = self.board, self.column_chars, self.row_nums
        char_ind, num_ind = columns.index(pos_char), rows.index(pos_num)

        row_from, row_to = self._get_loss_interval(num_ind)
        vertical = ""
        for i in range(row_from, row_to + 1):
            cell = board[pos_char][rows[i]]
            vertical += cell if cell else "-"
        return self._is_loss_line(vertical)

    def _check_diagonal(self, pos_char, pos_num):
        board, columns, rows = self.board, self.column_chars, self.row_nums
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

    def _loss_check(self, pos_char, pos_num):
        """Returns boolean value whether the player wins the game."""
        return (self._check_horizontal(pos_char, pos_num)) or \
               (self._check_vertical(pos_char, pos_num)) or \
               (self._check_diagonal(pos_char, pos_num))

    def _choose_first(self):
        """Randomly returns the player's mark that goes first."""
        return self.players_marks[random.choice((0, 1))]

    def _space_check(self, pos_char, pos_num):
        """Returns boolean value whether the cell is free or not."""
        return self.board[pos_char][pos_num] not in self.players_marks

    def _full_board_check(self):
        """Returns boolean value whether the game board is full of game marks."""
        for row in self.board.values():
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

    def _switch_player(self):
        """Switches player's marks to play next turn."""
        return 'O' if self.current_player_mark == 'X' else 'X'

    def _check_game_finish(self, pos_char, pos_num):
        """Return boolean value is the game finished or not."""
        if self._loss_check(pos_char, pos_num):
            winner = self._switch_player()
            print(f'The player with the mark "{winner}" wins!')
            return True

        if self._full_board_check():
            print('The game ended in a draw.')
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
    else:
        play_game = False

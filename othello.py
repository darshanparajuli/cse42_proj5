# Darshan Parajuli 16602518
# ICS 32 Fall 2015
# Project 5


# For debug purposes
import random


BLACK_PIECE = 1
WHITE_PIECE = 2


class _Cell:

    def __init__(self, row, col) -> None:
        self._row = row
        self._col = col
        self._piece = None

    def is_empty(self) -> bool:
        return self._piece == None

    def get_piece(self) -> 'piece type':
        return self._piece

    def set_piece(self, piece) -> None:
        self._piece = piece

    def get_row(self) -> int:
        return self._row

    def get_col(self) -> int:
        return self._col

    def __str__(self) -> None:
        return 'r: {}, c: {}'.format(self._row, self._col)

    def __eq__(self, other):
        return other and self._row == other._row and self._col == other._col and self._piece == other._piece

    def __hash__(self):
        return hash(self._row) ^ hash(self._col) ^ hash(self._piece)


class OthelloBoardOptions:

    def __init__(self) -> None:
        self._row_count = 16
        self._col_count = 16
        self._first_turn = BLACK_PIECE
        self._top_left_piece = WHITE_PIECE
        self._high_count_wins = True

    def get_row_count(self) -> int:
        return self._row_count

    def get_col_count(self) -> int:
        return self._col_count

    def get_first_turn(self) -> 'piece type':
        return self._first_turn

    def get_top_left_piece(self) -> 'piece type':
        return self._top_left_piece

    def high_count_wins(self) -> bool:
        return self._high_count_wins

    def set_row_count(self, row_count: int) -> None:
        self._row_count = row_count

    def set_col_count(self, col_count: int) -> None:
        self._col_count = col_count

    def set_high_count_wins(self, high_count_wins: bool) -> None:
        self._high_count_wins = high_count_wins

    def set_top_left_piece(self, top_left_piece: 'piece type') -> None:
        self._top_left_piece = top_left_piece

    def set_first_turn(self, first_turn: 'piece type') -> None:
        self._first_turn = first_turn


class OthelloBoard:

    def __init__(self, board_options: OthelloBoardOptions) -> None:
        self._board_options = board_options
        self._row_count = board_options._row_count
        self._col_count = board_options._col_count
        self._first_turn = board_options._first_turn
        self._board = self._init_board(board_options._top_left_piece)
        self._high_count_wins = board_options._high_count_wins
        self._possible_valid_moves = self._get_all_possible_valid_moves(board_options._first_turn)
        self._piece_count = self._get_piece_count()

        # For debug purposes
        self.print_row_col_labels = False

    def get_board_options(self) -> OthelloBoardOptions:
        return self._board_options

    def _init_board(self, top_left) -> [[_Cell]]:
        board = [[_Cell(row, col) for col in range(self._col_count)] for row in range(self._row_count)]

        r = int(self._row_count / 2 - 1)
        c = int(self._col_count / 2 - 1)
        if top_left == WHITE_PIECE:
            board[r][c].set_piece(WHITE_PIECE)
            board[r][c + 1].set_piece(BLACK_PIECE)
            board[r + 1][c].set_piece(BLACK_PIECE)
            board[r + 1][c + 1].set_piece(WHITE_PIECE)
        else:
            board[r][c].set_piece(BLACK_PIECE)
            board[r][c + 1].set_piece(WHITE_PIECE)
            board[r + 1][c].set_piece(WHITE_PIECE)
            board[r + 1][c + 1].set_piece(BLACK_PIECE)

        return board

    def print_board(self) -> None:
        if self.print_row_col_labels:
            print(' '.ljust(len(str(self._row_count))), end = ' ')
            for c in range(self._col_count):
                print(str(c + 1).ljust(len(str(self._col_count))), end = ' ')
            print()
        for r in range(self._row_count):
            if self.print_row_col_labels:
                print('{}'.format(r + 1).ljust(len(str(self._row_count))), end = ' ')
            for c in range(self._col_count):
                cell = self._board[r][c]
                cell_str = None
                if cell.get_piece() == BLACK_PIECE:
                    cell_str = 'B'
                elif cell.get_piece() == WHITE_PIECE:
                    cell_str = 'W'
                else:
                    cell_str = '.'

                ljust_val = None
                if self.print_row_col_labels:
                    ljust_val = len(str(self._col_count))
                else:
                    ljust_val = 0
                print(cell_str.ljust(ljust_val), end = ' ')
            print()

    def get_cell(self, row: int, col: int) -> _Cell:
        if row >= 0 and row < self._row_count:
            if col >= 0 and col < self._col_count:
                return self._board[row][col]
        return None

    def _get_cell_west(self, cell: _Cell) -> _Cell:
        return self.get_cell(cell.get_row(), cell.get_col() - 1)

    def _get_cell_east(self, cell: _Cell) -> _Cell:
        return self.get_cell(cell.get_row(), cell.get_col() + 1)

    def _get_cell_north(self, cell: _Cell) -> _Cell:
        return self.get_cell(cell.get_row() - 1, cell.get_col())

    def _get_cell_south(self, cell: _Cell) -> _Cell:
        return self.get_cell(cell.get_row() + 1, cell.get_col())

    def _get_cell_northwest(self, cell: _Cell) -> _Cell:
        return self.get_cell(cell.get_row() - 1, cell.get_col() - 1)

    def _get_cell_northeast(self, cell: _Cell) -> _Cell:
        return self.get_cell(cell.get_row() - 1, cell.get_col() + 1)

    def _get_cell_southwest(self, cell: _Cell) -> _Cell:
        return self.get_cell(cell.get_row() + 1, cell.get_col() - 1)

    def _get_cell_southeast(self, cell: _Cell) -> _Cell:
        return self.get_cell(cell.get_row() + 1, cell.get_col() + 1)

    def get_opponent_piece_type(self, piece_type: 'piece type') -> 'piece type':
        if piece_type == BLACK_PIECE:
            return WHITE_PIECE
        else:
            return BLACK_PIECE

    def place_piece(self, piece_type: 'piece type', row: int, col: int) -> bool:
        key = self._flatten_row_col(row, col)
        if key in self._possible_valid_moves:
            self._board[row][col].set_piece(piece_type)

            for captured_cell in self._possible_valid_moves[key][1]:
                captured_cell.set_piece(piece_type)

            self._piece_count = self._get_piece_count()
            self.skip_player_move(piece_type)
            return True
        return False

    def skip_player_move(self, piece_type: 'piece type') -> 'opponent piece type':
        opponent_piece = self.get_opponent_piece_type(piece_type)
        self._possible_valid_moves = self._get_all_possible_valid_moves(opponent_piece)
        # OthelloBoard._print_possible_moves(self._possible_valid_moves)
        return opponent_piece

    def get_possible_valid_moves_num(self, piece_type = None) -> int:
        if self._piece_count[0] == 0 or self._piece_count[1] == 0:
            return 0

        if piece_type == None:
            return len(self._possible_valid_moves.keys())
        else:
            return len(self._get_all_possible_valid_moves(piece_type).keys())

    def check_win(self) -> 'BLACK_PIECE, WHITE_PIECE or None':
        b_count = self._piece_count[0]
        w_count = self._piece_count[1]

        if self._high_count_wins:
            if b_count > w_count:
                return BLACK_PIECE
            elif b_count < w_count:
                return WHITE_PIECE
            else:
                return None
        else:
            if b_count < w_count:
                return BLACK_PIECE
            elif b_count > w_count:
                return WHITE_PIECE
            else:
                return None

    def get_piece_count(self, piece_type: 'piece type') -> int:
        if piece_type == BLACK_PIECE:
            return self._piece_count[0]
        else:
            return self._piece_count[1]

    def _get_piece_count(self) -> '(black_piece_count, white_piece_count)':
        b_count = 0
        w_count = 0
        for r in range(self._row_count):
            for c in range(self._col_count):
                cell = self._board[r][c]
                if cell.get_piece() == BLACK_PIECE:
                    b_count += 1
                elif cell.get_piece() == WHITE_PIECE:
                    w_count += 1

        return b_count, w_count

    # For debug purposes
    def _print_possible_moves(possible_valid_moves: {}) -> None:
        print('possible valid moves: ')
        for key in possible_valid_moves.keys():
            valid_cell, captured_cells = possible_valid_moves[key]
            print(str(valid_cell))

            for captured_cell in captured_cells:
                print('    {}'.format(str(captured_cell)))

    def _get_flattened_cell_pos(self, cell: _Cell) -> int:
        return self._flatten_row_col(cell.get_row(), cell.get_col())

    def _flatten_row_col(self, row: int, col: int) -> int:
        return row * self._col_count + col

    # For debug purposes... and for fun xD
    def get_ai_move(self, piece_type: 'piece type') -> '(row, col)':
        possible_valid_moves = self._get_all_possible_valid_moves(piece_type)
        keys = list(possible_valid_moves.keys())
        keys.sort(key = lambda k: len(possible_valid_moves[k][1]), reverse = True)
        keys_highest_captures = []
        highest_captures = len(possible_valid_moves[keys[0]][1])
        for k in keys:
            if len(possible_valid_moves[k][1]) == highest_captures:
                keys_highest_captures.append(k)
        valid_cell = possible_valid_moves[keys_highest_captures[random.randint(0, len(keys_highest_captures) - 1)]][0]
        return valid_cell.get_row(), valid_cell.get_col()

    def _get_all_possible_valid_moves(self, piece: 'piece type') -> {}:
        possible_valid_moves = {}

        for r in range(self._row_count):
            for c in range(self._col_count):
                cell = self._board[r][c]
                if cell.get_piece() != piece:
                    continue

                valid_cells = []
                valid_cells.append(self._get_possible_valid_moves(cell, self._get_cell_east))
                valid_cells.append(self._get_possible_valid_moves(cell, self._get_cell_west))
                valid_cells.append(self._get_possible_valid_moves(cell, self._get_cell_north))
                valid_cells.append(self._get_possible_valid_moves(cell, self._get_cell_south))
                valid_cells.append(self._get_possible_valid_moves(cell, self._get_cell_northeast))
                valid_cells.append(self._get_possible_valid_moves(cell, self._get_cell_northwest))
                valid_cells.append(self._get_possible_valid_moves(cell, self._get_cell_southeast))
                valid_cells.append(self._get_possible_valid_moves(cell, self._get_cell_southwest))

                for element in valid_cells:
                    if element != None:
                        valid_cell, captured_cells = element
                        key = self._get_flattened_cell_pos(valid_cell)
                        if key in possible_valid_moves:
                            for captured_cell in captured_cells:
                                possible_valid_moves[key][1].add(captured_cell)
                        else:
                            possible_valid_moves[key] = (valid_cell, set(captured_cells))

        return possible_valid_moves

    def _get_possible_valid_moves(self, cell: _Cell, f: 'direction function') -> '(valid cell, marked cells)':
        captured_cells = []
        piece_type = cell.get_piece()
        temp_cell = f(cell)
        while temp_cell != None:
            if temp_cell.is_empty():
                captured_cells.append(temp_cell)
                break
            if temp_cell.get_piece() == piece_type:
                break

            if temp_cell.get_piece() != piece_type:
                captured_cells.append(temp_cell)
            temp_cell = f(temp_cell)

        if len(captured_cells) > 1:
            top = captured_cells.pop()
            if top.is_empty():
                return top, captured_cells

import othello
import tkinter as tk


_BLACK_PIECE_LABEL = 'Black: {}'
_WHITE_PIECE_LABEL = 'White: {}'
_BOTTOM_LABEL = '{}: {}'
_HIGHER_SCORE_COLOR = '#43A047'
_LOWER_SCORE_COLOR = '#E53935'
_WINNER_COLOR = '#1E88E5'
_LOSER_COLOR = '#6D4C41'
_SAME_SCORE_COLOR = '#757575'


class SetupWindow:

    def __init__(self) -> None:
        pass

    def show() -> None:
        pass


class GameWindow:

    def __init__(self) -> None:
        self._othello_board_options = othello.OthelloBoardOptions()
        self._othello_board_options.set_row_count(8)
        self._othello_board_options.set_col_count(8)
        self._othello_board = othello.OthelloBoard(self._othello_board_options)
        self._current_player = self._othello_board_options.get_first_turn()
        self._root_window = tk.Tk()
        self._game_over = False
        self._root_window.wm_title("Othello - FULL")
        self._canvas = tk.Canvas(master = self._root_window,
                                 width = 400, height = 400,
                                 background = '#4CAF50')

        label_font = ("Monospace", 14)
        self._black_piece_label = tk.Label(master = self._root_window, font = label_font, fg = 'white',
                                           padx = 10, pady = 10)
        self._black_piece_label.grid(row = 0, column = 0,
                                     padx = (10, 5), pady = (10, 0),
                                     sticky = tk.E + tk.W + tk.N + tk.W)

        self._white_piece_label = tk.Label(master = self._root_window, font = label_font, fg = 'white',
                                           padx = 10, pady = 10)
        self._white_piece_label.grid(row = 0, column = 1,
                                     padx = (5, 10), pady = (10, 0),
                                     sticky = tk.E + tk.W + tk.N + tk.S)

        self._bottom_label = tk.Label(master = self._root_window, font = label_font, fg = 'white',
                                      bg = _SAME_SCORE_COLOR,
                                      padx = 10, pady = 10)
        self._bottom_label.grid(row = 2, column = 0, columnspan = 2,
                              padx = 10, pady = (0, 10),
                              sticky = tk.E + tk.W + tk.N + tk.S)

        self._canvas.grid(row = 1, column = 0, columnspan = 2,
                          padx = 10, pady = 10,
                          sticky = tk.E + tk.W + tk.N + tk.S)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        self._root_window.columnconfigure(1, weight = 1)

        self._root_window.bind('<Configure>', self._on_configure_event)
        self._canvas.bind('<Button-1>', self._on_left_mouse_clicked)

    def _get_turn_str(self, piece_type: 'piece type') -> 'player name':
        return 'Black' if piece_type == othello.BLACK_PIECE else 'White'

    def start(self) -> None:
        self._root_window.mainloop()

    def _on_configure_event(self, event: tk.Event) -> None:
        self._draw_canvas()
        self._update_labels()

    def _on_left_mouse_clicked(self, event: tk.Event) -> None:
        if self._game_over:
            return

        row_count = self._othello_board_options.get_row_count()
        col_count = self._othello_board_options.get_col_count()
        row = int(event.y / self._canvas.winfo_height() * row_count)
        col = int(event.x / self._canvas.winfo_width() * col_count)

        if self._othello_board.place_piece(self._current_player, row, col):
            self._current_player = self._othello_board.get_opponent_piece_type(self._current_player)
            if self._othello_board.get_possible_valid_moves_num() == 0:
                self._current_player = self._othello_board.skip_player_move(self._current_player)
                if self._othello_board.get_possible_valid_moves_num() == 0:
                    self._game_over = True

            self._draw_canvas()
            self._update_labels()

    def _update_labels(self) -> None:
        bcount = self._othello_board.get_piece_count(othello.BLACK_PIECE)
        wcount = self._othello_board.get_piece_count(othello.WHITE_PIECE)
        self._black_piece_label['text'] = _BLACK_PIECE_LABEL.format(bcount)
        self._white_piece_label['text'] = _WHITE_PIECE_LABEL.format(wcount)

        if self._game_over:
            winner = self._othello_board.check_win()
            text = None
            if winner == othello.BLACK_PIECE:
                text = 'Black'
                self._black_piece_label['bg'] = _WINNER_COLOR
                self._white_piece_label['bg'] = _LOSER_COLOR
            elif winner == othello.WHITE_PIECE:
                text = 'White'
                self._black_piece_label['bg'] = _LOSER_COLOR
                self._white_piece_label['bg'] = _WINNER_COLOR
            else:
                text = 'None'
                self._black_piece_label['bg'] = _LOSER_COLOR
                self._white_piece_label['bg'] = _LOSER_COLOR

            self._bottom_label['text'] = _BOTTOM_LABEL.format('Winner', text)
            self._bottom_label['bg'] = _WINNER_COLOR
        else:
            higher_score_color = _HIGHER_SCORE_COLOR
            lower_score_color = _LOWER_SCORE_COLOR
            if not self._othello_board_options.high_count_wins():
                higher_score_color = _LOWER_SCORE_COLOR
                lower_score_color = _HIGHER_SCORE_COLOR

            if bcount > wcount:
                self._black_piece_label['bg'] = higher_score_color
                self._white_piece_label['bg'] = lower_score_color
            elif wcount > bcount:
                self._black_piece_label['bg'] = lower_score_color
                self._white_piece_label['bg'] = higher_score_color
            else:
                self._black_piece_label['bg'] = _SAME_SCORE_COLOR
                self._white_piece_label['bg'] = _SAME_SCORE_COLOR

            self._bottom_label['text'] = _BOTTOM_LABEL.format('Turn', self._get_turn_str(self._current_player))
            self._bottom_label['bg'] = _SAME_SCORE_COLOR

    def _draw_canvas(self) -> None:
        self._canvas.delete(tk.ALL)

        cwidth = self._canvas.winfo_width()
        cheight = self._canvas.winfo_height()

        row_count = self._othello_board_options.get_row_count()
        col_count = self._othello_board_options.get_col_count()
        row_height = cheight / row_count
        col_width = cwidth / col_count
        offset = 5

        for row in range(row_count):
            for col in range(col_count):
                cell = self._othello_board.get_cell(row, col)
                if not cell.is_empty():
                    fill_color = 'white' if cell.get_piece() == othello.WHITE_PIECE else 'black'
                    self._canvas.create_oval(col * col_width + offset, row * row_height + offset,
                                             (col + 1) * col_width - offset, (row + 1) * row_height - offset,
                                             fill = fill_color, outline = '')


        for row in range(row_count):
            self._canvas.create_line(0, row_height * row, cwidth, row_height * row, fill = 'black')

        for col in range(col_count):
            self._canvas.create_line(col_width * col, 0, col_width * col, cheight, fill = 'black')

        self._canvas.create_rectangle(0, 0, cwidth, cheight, width = 5, outline = 'black')

# Darshan Parajuli 16602518
# ICS 32 Fall 2015
# Project 5


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


def _piece_to_str(piece_type: 'piece type') -> 'player name':
    return 'Black' if piece_type == othello.BLACK_PIECE else 'White'


class SetupWindow:

    _OPTION_WIN_CONDITIONS = {'Lowest piece count': False, 'Highest piece count': True}
    _OPTION_BLACK_WHITE = {'Black': othello.BLACK_PIECE, 'White': othello.WHITE_PIECE}
    _OPTION_PLAY_AGAINST = {'Human': False, 'Computer': True}

    def __init__(self, as_dialog = True, options = othello.OthelloBoardOptions()) -> None:
        self._as_dialog = as_dialog
        self._options = options
        self._ok_clicked = False

        self._dialog_window = tk.Toplevel() if as_dialog else tk.Tk()
        self._dialog_window.wm_title('Othello (FULL) - New game')

        label_font = ('Monospace', 12)
        om_font = ('Monospace', 10)

        tk.Label(self._dialog_window, text = 'Board size:', font = label_font).grid(
                row = 0, column = 0, sticky = tk.E)

        self._row_count_var = tk.StringVar()
        om_row_count = tk.OptionMenu(self._dialog_window, self._row_count_var, *[str(x) for x in range(4, 17, 2)])
        om_row_count.config(font = om_font)
        om_row_count.grid(row = 0, column = 1, sticky = tk.W)

        tk.Label(self._dialog_window, text = 'X', font = label_font).grid(row = 0, column = 2, sticky = tk.W + tk.E)

        self._col_count_var = tk.StringVar()
        om_col_count = tk.OptionMenu(self._dialog_window, self._col_count_var, *[str(x) for x in range(4, 17, 2)])
        om_col_count.config(font = om_font)
        om_col_count.grid(row = 0, column = 3, sticky = tk.W)

        bw = sorted(SetupWindow._OPTION_BLACK_WHITE.keys())

        tk.Label(self._dialog_window, text = 'First move:', font = label_font).grid(
                row = 1, column = 0, sticky = tk.E)

        self._first_turn_var = tk.StringVar()
        om_first_turn = tk.OptionMenu(self._dialog_window, self._first_turn_var, *bw)
        om_first_turn.config(font = om_font)
        om_first_turn.grid(row = 1, column = 1, columnspan = 3, sticky = tk.W)

        tk.Label(self._dialog_window, text = 'Top left:', font = label_font).grid(
                row = 2, column = 0, sticky = tk.E)

        self._top_left_var = tk.StringVar()
        om_top_left = tk.OptionMenu(self._dialog_window, self._top_left_var, *bw)
        om_top_left.config(font = om_font)
        om_top_left.grid(row = 2, column = 1, columnspan = 3, sticky = tk.W)

        tk.Label(self._dialog_window, text = 'Win condition:', font = label_font).grid(
                row = 3, column = 0, sticky = tk.E)

        self._win_condition_var = tk.StringVar()
        keys = list(SetupWindow._OPTION_WIN_CONDITIONS.keys())
        keys.sort()
        om_win_condition = tk.OptionMenu(self._dialog_window, self._win_condition_var, *keys)
        om_win_condition.config(font = om_font)
        om_win_condition.grid(row = 3, column = 1, columnspan = 3, sticky = tk.W)

        tk.Label(self._dialog_window, text = 'Play against:', font = label_font).grid(
                row = 4, column = 0, sticky = tk.E)

        self._play_against_var = tk.StringVar()
        keys = list(SetupWindow._OPTION_PLAY_AGAINST.keys())
        keys.sort()
        om_play_against = tk.OptionMenu(self._dialog_window, self._play_against_var, *keys)
        om_play_against.config(font = om_font)
        om_play_against.grid(row = 4, column = 1, columnspan = 3, sticky = tk.W)

        tk.Button(self._dialog_window, text = 'OK', command = self._on_ok_clicked).grid(row = 5, column = 2)
        tk.Button(self._dialog_window, text = 'Cancel', command = self._on_cancel_clicked).grid(
                row = 5, column = 3, padx = 10, pady = 10)

        self._init_defaults()
        self._init_callbacks()

    def _init_callbacks(self) -> None:
        self._row_count_var.trace('w', self._on_row_count_changed)
        self._col_count_var.trace('w', self._on_col_count_changed)
        self._first_turn_var.trace('w', self._on_first_turn_changed)
        self._top_left_var.trace('w', self._on_top_left_changed)
        self._win_condition_var.trace('w', self._on_win_condition_changed)
        self._play_against_var.trace('w', self._on_play_against_changed)

    def _init_defaults(self) -> None:
        self._row_count_var.set(str(self._options.get_row_count()))
        self._col_count_var.set(str(self._options.get_col_count()))
        self._first_turn_var.set(_piece_to_str(self._options.get_first_turn()))
        self._top_left_var.set(_piece_to_str(self._options.get_top_left_piece()))
        keys = list(SetupWindow._OPTION_WIN_CONDITIONS.keys())
        keys.sort()
        self._win_condition_var.set(keys[0 if self._options.high_count_wins() else 1])
        keys = list(SetupWindow._OPTION_PLAY_AGAINST.keys())
        keys.sort()
        self._play_against_var.set(keys[0 if self._options.play_against_ai() else 1])

    def _on_row_count_changed(self, *args) -> None:
        self._options.set_row_count(int(self._row_count_var.get()))

    def _on_col_count_changed(self, *args) -> None:
        self._options.set_col_count(int(self._col_count_var.get()))

    def _on_first_turn_changed(self, *args) -> None:
        first_turn = self._first_turn_var.get()
        self._options.set_first_turn(SetupWindow._OPTION_BLACK_WHITE[first_turn])

    def _on_top_left_changed(self, *args) -> None:
        top_left = self._top_left_var.get()
        self._options.set_top_left_piece(SetupWindow._OPTION_BLACK_WHITE[top_left])

    def _on_win_condition_changed(self, *args) -> None:
        win_condition = self._win_condition_var.get()
        self._options.set_high_count_wins(SetupWindow._OPTION_WIN_CONDITIONS[win_condition])

    def _on_play_against_changed(self, *args) -> None:
        play_against = self._play_against_var.get()
        self._options.set_play_against_ai(SetupWindow._OPTION_PLAY_AGAINST[play_against])

    def _on_ok_clicked(self) -> None:
        self._ok_clicked = True
        self._dialog_window.destroy()

        if not self._as_dialog:
            GameWindow(self._options).start()

    def _on_cancel_clicked(self) -> None:
        self._dialog_window.destroy()

    def start(self) -> None:
        if self._as_dialog:
            self._dialog_window.grab_set()
            self._dialog_window.wait_window()
        else:
            self._dialog_window.mainloop()

    def ok(self) -> bool:
        return self._ok_clicked

    def get_othello_board_options(self) -> othello.OthelloBoardOptions:
        return self._options


class GameWindow:

    def __init__(self, options: othello.OthelloBoardOptions) -> None:
        self._init_game_state(options)
        self._ai_thinking = False
        self._root_window = tk.Tk()
        self._root_window.wm_title("Othello (FULL)")
        self._canvas = tk.Canvas(master = self._root_window,
                                 width = 400, height = 400,
                                 background = '#4CAF50')
        self._canvas.grid(row = 1, column = 0, columnspan = 2,
                          padx = 10, pady = 10,
                          sticky = tk.E + tk.W + tk.N + tk.S)

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
        self._bottom_label.grid(row = 2, column = 1,
                              padx = 10, pady = (0, 10),
                              sticky = tk.E + tk.W + tk.N + tk.S)

        self._new_game_button = tk.Button(master = self._root_window, font = label_font,
                text = 'New game', command = self._show_setup_dialog).grid(
                        row = 2, column = 0, sticky = tk.E + tk.W + tk.N + tk.S, padx = (10, 0), pady = (0, 10))

        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)
        self._root_window.columnconfigure(1, weight = 1)

        self._root_window.bind('<Configure>', self._on_configure_event)
        self._canvas.bind('<Button-1>', self._on_left_mouse_clicked)

    def _init_game_state(self, options: othello.OthelloBoardOptions) -> None:
        self._othello_board_options = options
        self._othello_board = othello.OthelloBoard(options)
        self._current_player = options.get_first_turn()
        self._ai_player = self._othello_board.get_opponent_piece_type(self._current_player)
        self._game_over = False

    def _show_setup_dialog(self) -> None:
        setup_window = SetupWindow(self._othello_board_options)
        setup_window.start()
        if setup_window.ok():
            self._init_game_state(setup_window.get_othello_board_options())
            self._draw_canvas()
            self._update_labels()

    def start(self) -> None:
        self._root_window.mainloop()

    def _on_configure_event(self, event: tk.Event) -> None:
        self._draw_canvas()
        self._update_labels()

    def _on_left_mouse_clicked(self, event: tk.Event) -> None:
        if self._game_over or self._ai_thinking:
            return

        row_count = self._othello_board_options.get_row_count()
        col_count = self._othello_board_options.get_col_count()
        row = int(event.y / self._canvas.winfo_height() * row_count)
        col = int(event.x / self._canvas.winfo_width() * col_count)

        self._insert_piece(row, col)

        if self._othello_board_options.play_against_ai() and self._current_player == self._ai_player:
            self._ai_thinking = True
            self._update_labels()
            self._root_window.after(1000, self._execute_ai_move)

    def _execute_ai_move(self) -> None:
        self._ai_thinking = False
        row, col = self._othello_board.get_ai_move(self._current_player)
        self._insert_piece(row, col)

    def _insert_piece(self, row: int, col: int) -> None:
        if self._othello_board.place_piece(self._current_player, row, col):
            # if self._current_player == self._ai_player:
            #     print('ai moved')
            # else:
            #     print('player moved')
            self._current_player = self._othello_board.get_opponent_piece_type(self._current_player)
            if self._othello_board.get_possible_valid_moves_num() == 0:
                self._current_player = self._othello_board.skip_player_move(self._current_player)
                if self._othello_board.get_possible_valid_moves_num() == 0:
                    self._game_over = True
                else:
                    if self._othello_board_options.play_against_ai() and self._current_player == self._ai_player:
                        self._ai_thinking = True
                        self._root_window.after(1000, self._execute_ai_move)
                        # print('ai moved again')

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

            if self._othello_board_options.play_against_ai() and self._ai_thinking:
                self._bottom_label['text'] = 'Thinking...'
            else:
                self._bottom_label['text'] = _BOTTOM_LABEL.format('Turn', _piece_to_str(self._current_player))
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

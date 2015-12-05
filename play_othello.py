import gui


def main() -> None:
    setup_window = gui.SetupWindow(False) # False: start as the mainwindow in the beginning
    setup_window.start()

if __name__ == '__main__':
    main()

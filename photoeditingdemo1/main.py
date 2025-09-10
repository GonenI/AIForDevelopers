from __future__ import annotations


def main() -> None:
    from photoedit.ui.main_window import MainWindow
    root = MainWindow()
    root.mainloop()


if __name__ == "__main__":
    main()

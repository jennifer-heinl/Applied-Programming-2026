
import sys

from PySide6.QtWidgets import QApplication

from views.mainView import MainView
from viewmodels.mainViewModel import MainViewModel


def main():
    app = QApplication(sys.argv)

    # TODO 1:
    # Create the ViewModel object.
    view_model = MainViewModel()

    # TODO 2:
    # Create the MainView and pass the ViewModel into it.
    view = MainView(view_model)

    # TODO 3:
    # Show the window.
    view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
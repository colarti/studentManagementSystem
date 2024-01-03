from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit
import sys


class AgeCalc(QWidget):
    def __init__(self):
        super().__init__()
        grid = QGridLayout()

        name_lbl = QLabel('Name')
        name_txtbox = QLineEdit()

        birthdate_lbl = QLabel('Birthday (MM/DD/YYYY)')
        birthdate_txtbox = QLineEdit()

        grid.addWidget(name_lbl, 0, 0)
        grid.addWidget(name_txtbox, 0, 1)
        grid.addWidget(birthdate_lbl, 1, 0)
        grid.addWidget(birthdate_txtbox, 1, 1)

        self.setLayout(grid)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    age_calc = AgeCalc()
    age_calc.show()
    sys.exit(app.exec())

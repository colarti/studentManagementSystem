from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, \
QGridLayout, QLineEdit, QPushButton
import sys
from datetime import datetime


class AgeCalc(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Age Calculator')
        grid = QGridLayout()

        # Create Widgets
        name_lbl = QLabel('Name')
        self.name_txtbox = QLineEdit()

        birthdate_lbl = QLabel('Birthday (MM/DD/YYYY)')
        self.birthdate_txtbox = QLineEdit()

        calc_btn = QPushButton('Calculate Age')
        calc_btn.clicked.connect(self.calculate_age)
        self.output_lbl = QLabel('')

        # Attach Widgets to Grid
        grid.addWidget(name_lbl, 0, 0)
        grid.addWidget(self.name_txtbox, 0, 1)
        grid.addWidget(birthdate_lbl, 1, 0)
        grid.addWidget(self.birthdate_txtbox, 1, 1)
        grid.addWidget(calc_btn, 2, 0, 1, 2)   #row, col, span of rows, span of columns
        grid.addWidget(self.output_lbl, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_age(self):
        today = datetime.today().year
        print(f'today: {today}')
        
        birthdate = datetime.strptime(self.birthdate_txtbox.text() , '%m/%d/%Y').date().year
        print(f'birthdate: {birthdate}')

        age = today - birthdate
        print(f'age: {age}')
        self.output_lbl.setText(f'{self.name_txtbox.text()} is {age} years old')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    age_calc = AgeCalc()
    age_calc.show()
    sys.exit(app.exec())

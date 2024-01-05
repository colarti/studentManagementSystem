from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout,\
    QLineEdit, QPushButton, QComboBox, QMenuBar, QMainWindow, QTableWidget,\
    QTableWidgetItem, QDialog, QVBoxLayout
from PyQt6.QtGui import QAction
import sys
import sqlite3 as sql



class StudentManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        grid = QGridLayout()

        # Create Widgets
        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')
        
        add_student_action = QAction('Add Student', self)
        add_student_action.triggered.connect(self.add_person)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)
        # about_action.setMenuRole(QAction.MenuRole.NoRole)  #meant for mac users

        search_student_action = QAction('Search Student', self)
        search_student_action.triggered.connect(self.search_person)
        edit_menu_item.addAction(search_student_action)


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False) #remove the vertical numbers, since ID has the number
        self.load_data()    #populate the table

        self.setCentralWidget(self.table)


    def add_person(self):
        dialog = InsertDialog()
        dialog.exec()

    def search_person(self):
        search_dialog = SearchDialog()
        search_dialog.exec()

    def delete_person(self):
        pass

    def edit_person(self):
        pass

    def load_data(self):
        connection = sql.connect('database.db')
        data = connection.execute('SELECT * FROM students')
        
        self.table.setRowCount(0)   #resets the table and loads starting from 0,0

        for row_number, row_data in enumerate(data.fetchall()):
            self.table.insertRow(row_number)
            # print(f'row_num: {row_number}   row_data:{row_data}')
            for column_num, data in enumerate(row_data):
                # print(f'col_num: {column_num}    data:{data}')
                self.table.setItem(row_number, column_num, QTableWidgetItem(str(data)))
        connection.close()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Person')
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        grid = QVBoxLayout()

        self.txtbox_name = QLineEdit()
        self.txtbox_name.setPlaceholderText('Name')

        self.lbl_result = QLabel('')

        btn_search = QPushButton('Search')
        btn_search.clicked.connect(self.search_person)


        grid.addWidget(self.txtbox_name)
        grid.addWidget(self.lbl_result)
        grid.addWidget(btn_search)

        self.setLayout(grid)


    def search_person(self):
        connection = sql.connect('database.db')
        cursor = connection.cursor()
        # result = cursor.execute('SELECT * FROM students WHERE name LIKE ')
        cursor.close()
        connection.close()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Student')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        #create a layout
        grid = QVBoxLayout()
        # create a textbox for name
        self.txtbox_name = QLineEdit()
        self.txtbox_name.setPlaceholderText('Name')
        # create a combo box for courses
        self.combo_course = QComboBox()
        self.combo_course.addItems(['Math', 'Physics', 'Biology', 'Astronomy'])
        # create a text for phone number
        self.txtbox_mobile = QLineEdit()
        self.txtbox_mobile.setPlaceholderText('Mobile Number')
        # create a push button for submit
        btn_submit = QPushButton('Submit')
        btn_submit.clicked.connect(self.include_person)

        # add widgets to layout
        grid.addWidget(self.txtbox_name)
        grid.addWidget(self.combo_course)
        grid.addWidget(self.txtbox_mobile)
        grid.addWidget(btn_submit)

        # show the layout
        self.setLayout(grid)

    def include_person(self):
        connection = sql.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)', \
                       (self.txtbox_name.text(), self.combo_course.itemText(self.combo_course.currentIndex()), self.txtbox_mobile.text()))
        connection.commit()
        cursor.close()
        connection.close()

        student_manage.load_data()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    student_manage = StudentManagement()
    student_manage.show()
    sys.exit(app.exec())
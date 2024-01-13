from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout,\
    QLineEdit, QPushButton, QComboBox, QMenuBar, QMainWindow, QTableWidget,\
    QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar, QMessageBox\

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3 as sql


class DatabaseConnection:
    def __init__(self, file='database.db'):
        self.file = file
    
    def connect(self):
        self.connection = sql.connect(self.file)


class StudentManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        self.setMinimumSize(800,600)

        # Create Widgets
        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')
        
        add_student_action = QAction(QIcon('.\\icons\\add.png'), 'Add Student', self)
        add_student_action.triggered.connect(self.add_person)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)
        # about_action.setMenuRole(QAction.MenuRole.NoRole)  #meant for mac users
        about_action.triggered.connect(self.about_app)



        search_student_action = QAction(QIcon('.\\icons\\search.png'), 'Search Student', self)
        search_student_action.triggered.connect(self.search_person)
        edit_menu_item.addAction(search_student_action)


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False) #remove the vertical numbers, since ID has the number
        self.load_data()    #populate the table

        self.setCentralWidget(self.table)

        # create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        # add actions to toolbar
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # create status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        # add elements to status bar
        self.table.cellClicked.connect(self.show_status_elements)
        
        
    def about_app(self):
        dialog = AboutDialog()
        dialog.exec()

    def add_person(self):
        dialog = InsertDialog()
        dialog.exec()

    def search_person(self):
        search_dialog = SearchDialog()
        search_dialog.exec()

    def show_status_elements(self):
        btnEdit = QPushButton('Edit')
        btnEdit.clicked.connect(self.edit_person)

        btnDelete = QPushButton('Delete')
        btnDelete.clicked.connect(self.delete_person)

        #clear any other unwanted elements
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
        
        #add the pushbutton elements back to the status bar
        self.statusbar.addWidget(btnEdit)
        self.statusbar.addWidget(btnDelete)
    
    def unshow_status_elements(self):
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

    def delete_person(self):
        delete_dialog = DeleteDialog2()
        delete_dialog.exec()

    def edit_person(self):
        edit_dialog = EditDialog()
        edit_dialog.exec()

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


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About the App')
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        content = '''
This app is created to manage students
        '''
        self.setText(content)


class DeleteDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete Person')
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        self.setText('Are you sure you want to delete')
        self.setStandardButtons(QMessageBox.StandardButton.Yes |
                                QMessageBox.StandardButton.No)


        

        student_manage.load_data()
        self.close()


    def delete(self):      
        connection = sql.connect('database.db')
        cursor = connection.cursor()
        select = student_manage.table.currentRow()
        id = student_manage.table.item(select, 0).text()
        name = student_manage.table.item(select, 1).text()
        course = student_manage.table.item(select, 2).text()
        phone = student_manage.table.item(select, 3).text()

        cursor.execute('DELETE FROM students WHERE name = ?', (name,))
        
        connection.commit()
        cursor.close()
        connection.close()
        self.close()

        student_manage.unshow_status_elements()


        # confirmation = QMessageBox()
        # confirmation.setWindowTitle('Confirmation Widget')
        # confirmation.setText('Delete Successful')

        
    
class DeleteDialog2(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete Person')

        grid = QGridLayout()

        lbl_confirm = QLabel('Are you sure you want to delete?')

        btn_yes = QPushButton('Yes')
        btn_yes.clicked.connect(self.delete2)

        btn_no = QPushButton('No')
        btn_no.clicked.connect(self.close_window)
    
        grid.addWidget(lbl_confirm, 0,0,1,2)
        grid.addWidget(btn_yes, 1,0)
        grid.addWidget(btn_no, 1,1)

        self.setLayout(grid)

    def delete2(self):
        connection = sql.connect('database.db')
        cursor = connection.cursor()

        select = student_manage.table.currentRow()
        id = student_manage.table.item(select, 0).text()
        name = student_manage.table.item(select, 1).text()
        course = student_manage.table.item(select, 2).text()
        phone = student_manage.table.item(select, 3).text()

        cursor.execute('DELETE FROM students WHERE name = ?', (name,))
        connection.commit()
        cursor.close()
        connection.close()

        student_manage.load_data()
        self.close()
        student_manage.unshow_status_elements()

        col = student_manage.table.currentColumn()
        student_manage.table.item(select, col ).setSelected(False)

        confirm = QMessageBox()
        confirm.setWindowTitle('Delete Confirmation')
        confirm.setText('The record was deleted successfully')
        confirm.exec()

            
    def close_window(self):
        select = student_manage.table.currentRow()
        col = student_manage.table.currentColumn()
        student_manage.table.item(select, col ).setSelected(False)

        self.close()
        student_manage.unshow_status_elements()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Edit Person')
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        grid = QVBoxLayout()

        select = student_manage.table.currentRow()
        self.id = student_manage.table.item(select, 0).text()
        name = student_manage.table.item(select, 1).text()
        course = student_manage.table.item(select, 2).text()
        phone = student_manage.table.item(select, 3).text()


        self.txtbox_name = QLineEdit(name)

        self.combo_course = QComboBox()
        courses = ['Math', 'Physics', 'Biology', 'Astronomy']
        self.combo_course.addItems(courses)
        self.combo_course.setCurrentIndex(courses.index(course))

        self.txtbox_phone = QLineEdit(phone)

        btn_submit = QPushButton('Submit')
        btn_submit.clicked.connect(self.edit_record)

        grid.addWidget(self.txtbox_name)
        grid.addWidget(self.combo_course)
        grid.addWidget(self.txtbox_phone)
        grid.addWidget(btn_submit)

        self.setLayout(grid)

    
    def edit_record(self):
        connection = sql.connect('database.db')
        cursor = connection.cursor()
        
        cursor.execute('UPDATE students SET name = ?, course = ?, mobile = ? WHERE id=?', 
                       (self.txtbox_name.text(), self.combo_course.itemText(self.combo_course.currentIndex()), self.txtbox_phone.text(), self.id))
        connection.commit()
        cursor.close()
        connection.close()

        #reload the data into the table
        student_manage.load_data()

        #quit this element/widget
        self.close()

        student_manage.unshow_status_elements()

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
        name = self.txtbox_name.text()

        connection = sql.connect('database.db')
        cursor = connection.cursor()
        result = cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
        rows = list(result)

        items = student_manage.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            student_manage.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()

        self.close()

        

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
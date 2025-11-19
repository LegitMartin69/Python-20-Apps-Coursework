from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QComboBox, QWidget, QApplication, QLabel, QLineEdit, QPushButton,
                             QGridLayout, QMainWindow, QTableWidget, QTableWidgetItem, QDialog,
                             QVBoxLayout, QToolBar, QStatusBar, QMessageBox)
from PyQt6.QtGui import QAction, QIcon
import sqlite3
import sys


# TODO remove code smell - all those database connection calls


class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        self.database = database_file

    def connect(self):
        connection = sqlite3.connect(self.database)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(450, 400)

        # Dropdown setup
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Dropdown Action setup
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)

        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # Main Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Statusbar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

        self.load_data()


    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def load_data(self):
        """Load data from database"""
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM students")
        # Prevents duplicate
        self.table.setRowCount(0)

        # Iterates through the database
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            # print(row_data)
            for column_number, data in enumerate(row_data):
                # print(data)
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()
        print("DEBUG: Data Loaded")

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Window Settings
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Layout object instantiation
        layout = QVBoxLayout()

        # Student name input field
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student's name")
        layout.addWidget(self.student_name)

        # Course Combo Box
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Mobile input field
        self.mobile_number = QLineEdit()
        self.mobile_number.setPlaceholderText("Mobile phone number")
        layout.addWidget(self.mobile_number)

        # Submit Button
        button = QPushButton("Register Student")
        layout.addWidget(button)
        button.clicked.connect(self.add_student)

        # Set Layout
        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_number.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)"
                       ,(name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Window Settings
        self.setWindowTitle("Search for a specific record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Layout object instantiation
        layout = QVBoxLayout()

        # Search input field
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search for...")
        layout.addWidget(self.search_field)

        # Search Button
        search_button = QPushButton("Search")
        layout.addWidget(search_button)
        search_button.clicked.connect(self.find_student)

        # Set Layout
        self.setLayout(layout)

    def find_student(self):
        # local variables assignment
        name = self.search_field.text()
        # SQL Query
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name, ))
        rows = list(result)
        print(rows)
        # Flag matches the string
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)
        pass


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Window Settings
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Layout object instantiation
        layout = QVBoxLayout()

        # Getting current row info
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()
        course_name = main_window.table.item(index, 2).text()
        mobile_number = main_window.table.item(index, 3).text()

        # Get id from selected row
        self.student_id = main_window.table.item(index, 0).text()

        # Student name input field
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Student's name")
        layout.addWidget(self.student_name)

        # Course Combo Box
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Mobile input field
        self.mobile_number = QLineEdit(mobile_number)
        self.mobile_number.setPlaceholderText("Mobile phone number")
        layout.addWidget(self.mobile_number)

        # Submit Button
        button = QPushButton("Register Student")
        layout.addWidget(button)
        button.clicked.connect(self.update_student)

        # Set Layout
        self.setLayout(layout)

    def update_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_number.text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?"
                       , (name, course, mobile, self.student_id))
        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        super().__init__()
        # Window Settings
        self.setWindowTitle("Delete Student Data")

        # Layout object instantiation
        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?...")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        yes.clicked.connect(self.delete_student)

        # Set Layout
        self.setLayout(layout)

    def delete_student(self):
        # Get id from selected row
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?",
                       (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was successfully deleted")
        confirmation_widget.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created during the "The Python Mega Course",
        Its a simple demonstration of working with sqlite3 and PyQt6 libraries
        The app was made to store simple information about students
        and to easily view, edit and delete said information"""
        self.setText(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


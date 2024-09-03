import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QMessageBox, QMenuBar, QMenu, QTabWidget, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QHBoxLayout
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QFile, QTextStream

import student_service

class TextEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.text_edit = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            file = QFile(file_name)
            if file.open(QFile.ReadOnly | QFile.Text):
                text_stream = QTextStream(file)
                self.text_edit.setText(text_stream.readAll())
                file.close()

    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            file = QFile(file_name)
            if file.open(QFile.WriteOnly | QFile.Text):
                text_stream = QTextStream(file)
                text_stream << self.text_edit.toPlainText()
                file.close()

class StudentList(QWidget):
    def __init__(self):
        super().__init__()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter student name")

        self.address_input = QLineEdit(self)
        self.address_input.setPlaceholderText("Enter student address")

        self.add_button = QPushButton("Add Student", self)
        self.add_button.clicked.connect(self.add_student)

        self.delete_button = QPushButton("Delete Selected", self)
        self.delete_button.clicked.connect(self.delete_student)

        self.student_list = QListWidget(self)
        self.load_students()

        layout = QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.address_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        layout.addWidget(self.student_list)

        self.setLayout(layout)

    def load_students(self):
        students = student_service.get_students()
        for student in students:
            self.student_list.addItem(f"{student['name']} - {student['address']}")

    def add_student(self):
        name = self.name_input.text()
        address = self.address_input.text()

        if name and address:
            student_service.save_student(name, address)
            self.student_list.addItem(f"{name} - {address}")
            self.name_input.clear()
            self.address_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter both name and address")

    def delete_student(self):
        selected_items = self.student_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "Please select a student to delete")
            return

        for item in selected_items:
            self.student_list.takeItem(self.student_list.row(item))
            name, address = item.text().split(' - ')
            student_service.delete_student(name, address)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Multi-Tool Application')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("sample-icon.png"))

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.text_editor_tab = TextEditor()
        self.student_list_tab = StudentList()

        self.tabs.addTab(self.text_editor_tab, "Text Editor")
        self.tabs.addTab(self.student_list_tab, "Student List")

        # Create Menu Bar
        menu_bar = self.menuBar()
        self.setMenuBar(menu_bar)

        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        new_action = QAction("New", self)
        new_action.triggered.connect(self.text_editor_tab.text_edit.clear)
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.text_editor_tab.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.text_editor_tab.save_file)
        file_menu.addAction(save_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

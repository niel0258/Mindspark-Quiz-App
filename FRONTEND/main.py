import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget, QMessageBox, QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from pathlib import Path
backend_dir = Path(__file__).resolve().parent / ".." / "BACKEND"
sys.path.insert(0, str(backend_dir))

import styles as st
from users import initialize_storage
from qLoginUI import LoginUI
from qTeacherLandingUI import TeacherQuizLandingUI
from qStudentLandingUI import StudentQuizLandingUI
from qCreateUI import QuizEditor
from qTakeUI import QuizApp
from qResultsUI import QuizResultWindow
from database import initialize_quiz_storage, get_all_quizzes

class MainApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        initialize_storage()
        initialize_quiz_storage()

        self.stack = QStackedWidget()
        self.stack.resize(1280, 720)
        self.stack.setWindowTitle("MindSpark")
        self.stack.setWindowIcon(QIcon(str("logo.png")))

        self.login_ui = LoginUI()
        self.login_ui.logged_in.connect(self.handle_login)
        self.stack.addWidget(self.login_ui)

        self.stack.setCurrentWidget(self.login_ui)
        self.stack.show()

    def handle_login(self, username, role):
        if role.lower() == "teacher":
            self.landing_ui = TeacherQuizLandingUI()
            self.landing_ui.create_btn.setText("Create Quiz")
            self.landing_ui.create_btn.clicked.disconnect() if self.landing_ui.create_btn.receivers(self.landing_ui.create_btn.clicked) > 0 else None
            self.landing_ui.create_btn.clicked.connect(lambda: self.open_quiz_creator(username))
            self.landing_ui.sign_out_btn.clicked.connect(self.return_to_login)
            self.landing_ui.nav_quizzes.clicked.connect(lambda: self.show_quizzes_popup(username, "teacher"))
            self.landing_ui.nav_home.clicked.connect(lambda: self.reset_to_landing(username, role))
        else:
            self.landing_ui = StudentQuizLandingUI()
            self.landing_ui.play_btn.setText("Quizzes to Take")
            self.landing_ui.play_btn.clicked.disconnect() if self.landing_ui.play_btn.receivers(self.landing_ui.play_btn.clicked) > 0 else None
            self.landing_ui.play_btn.clicked.connect(lambda: self.show_quizzes_popup(username, "student"))
            self.landing_ui.sign_out_btn.clicked.connect(self.return_to_login)
            self.landing_ui.nav_quizzes.clicked.connect(lambda: self.show_quizzes_popup(username, "student"))
            self.landing_ui.nav_home.clicked.connect(lambda: self.reset_to_landing(username, role))

        self.stack.addWidget(self.landing_ui)
        self.stack.setCurrentWidget(self.landing_ui)

    def show_quizzes_popup(self, username, role):
        quizzes = get_all_quizzes()
        if not quizzes:
            QMessageBox.information(self.landing_ui, "No Quizzes", "No quizzes are currently available in the system.")
            return

        dialog = QWidget()
        dialog.setWindowTitle("Quizzes List")
        dialog.resize(500, 400)
        dialog.setStyleSheet(st.MAIN_WINDOW)
        v = QVBoxLayout(dialog)

        lbl = QLabel("Select a Quiz:" if role == "student" else "Quizzes Made:")
        lbl.setStyleSheet(st.LABEL_TITLE)
        v.addWidget(lbl)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        c_layout = QVBoxLayout(container)

        for q in quizzes:
            q_id, q_name, subj, creator = q
            
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            
            btn_text = f"Quiz: {q_name} | Subject: {subj} (By: {creator})"
            btn = QPushButton(btn_text)
            btn.setStyleSheet(st.BTN_PRIMARY)
            
            if role == "student":
                btn.clicked.connect(lambda checked, qid=q_id, un=username, d=dialog: self.start_taking_quiz(un, qid, d))
            else:
                btn.clicked.connect(lambda checked, qid=q_id, un=username, d=dialog: self.start_taking_quiz(un, qid, d))
            
            row_layout.addWidget(btn, 1)
            
            # Add delete button for teachers
            if role.lower() == "teacher":
                del_btn = QPushButton("Delete")
                del_btn.setStyleSheet(st.BTN_ROUND_DELETE if hasattr(st, "BTN_ROUND_DELETE") else st.BTN_PRIMARY)
                del_btn.setFixedSize(70, 30)
                del_btn.clicked.connect(lambda checked, qid=q_id, d=dialog, un=username, r=role: self.confirm_delete_quiz(qid, d, un, r))
                row_layout.addWidget(del_btn)
                
            c_layout.addWidget(row_widget)

        scroll.setWidget(container)
        v.addWidget(scroll)
        dialog.show()
        self.active_quiz_list_window = dialog

    def open_quiz_creator(self, username):
        self.creator_win = QuizEditor("", "", username)
        self.creator_win.show()
        self.creator_win.destroyed.connect(lambda: self.reset_to_landing(username, "Teacher"))

    def start_taking_quiz(self, username, quiz_id, dialog_to_close):
        dialog_to_close.close()
        self.take_win = QuizApp(quiz_id=quiz_id, username=username)
        self.take_win.quiz_submitted.connect(self.show_results)
        self.take_win.show()

    def show_results(self, username, quiz_id):
        self.result_win = QuizResultWindow(username=username, quiz_id=quiz_id)
        self.result_win.show()

    def confirm_delete_quiz(self, quiz_id, dialog, username, role):
        reply = QMessageBox.question(
            dialog,
            "Confirm Deletion", 
            "Are you sure you want to delete this quiz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            from database import delete_quiz_from_db
            if delete_quiz_from_db(quiz_id):
                QMessageBox.information(dialog, "Success", "Quiz deleted successfully.")
                if dialog:
                    dialog.close()
                self.show_quizzes_popup(username, role)
            else:
                QMessageBox.critical(dialog, "Error", "Failed to delete quiz from the database.")

    def reset_to_landing(self, username, role):
        self.handle_login(username, role)

    def return_to_login(self):
        self.login_ui.reset()
        self.stack.setCurrentWidget(self.login_ui)

if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec())

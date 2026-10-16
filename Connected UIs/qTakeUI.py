import sys
import csv
from pathlib import Path
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QRadioButton, QFrame, QButtonGroup, QScrollArea, QMessageBox
)

import styles as st
from database import get_quiz_details, save_student_result

class QuizApp(QMainWindow):
    quiz_submitted = pyqtSignal(str, int) # emits (username, quiz_id)

    def __init__(self, quiz_id=1, username="student"):
        super().__init__()
        self.setWindowTitle("Quiz Taking")
        self.resize(1280, 720)
        self.setObjectName("root")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(st.MAIN_WINDOW)

        self.quiz_id = quiz_id
        self.username = username
        self.quiz_title, self.subject_name = "Quiz name", "Subject name"

        q_info, raw_questions = get_quiz_details(quiz_id)
        if q_info:
            self.quiz_title, self.subject_name = q_info

        self.questions = self.parse_questions(raw_questions)
        self.totalQuestions = len(self.questions)
        self.currentQuestion = 0

        self.user_answers = {}
        self.option_frames = []
        self.nav_buttons = []

        if self.totalQuestions == 0:
            QMessageBox.critical(self, "Error", "No questions found for this quiz in the database.")
            sys.exit(1)

        self.UI()
        self.display_question(self.currentQuestion)

    def parse_questions(self, raw_questions):
        questions = []
        for row in raw_questions:
            q_type = "Multiple Choice" if row["type"] == "Multiple_Choice" else "True or False"
            options = row["choices"]
            
            correct_val = row["correct"]
            if isinstance(correct_val, int) and 0 <= correct_val < len(options):
                correct_str = options[correct_val]
            else:
                correct_str = str(correct_val)

            questions.append({
                "type": q_type,
                "question": row["question"],
                "options": options,
                "correct": correct_str,
                "correct_idx": row["correct"],
                "points": row["points"]
            })
        return questions

    def UI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        outer = QVBoxLayout(central_widget)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        
        outer.addWidget(self._build_header(self.quiz_title, self.subject_name))

        body = QHBoxLayout()
        body.setContentsMargins(26, 34, 26, 12)
        body.setSpacing(55)
        body.addLayout(self._build_left(), 1)
        body.addLayout(self._build_right())
        outer.addLayout(body, 1)
        outer.addLayout(self._build_footer())

    def _build_header(self, quiz_name, subject):
        header = QFrame()
        header.setStyleSheet(st.HEADER_CONTAINER)
        header.setFixedHeight(82)
        h = QVBoxLayout(header)
        h.setContentsMargins(48, 8, 20, 8)
        h.setSpacing(0)
        
        self.quiz_name_label = QLabel(quiz_name)
        self.quiz_name_label.setStyleSheet("font-size: 26px; font-weight: bold; color: white; border: none;")
        
        self.subject_label = QLabel(subject)
        self.subject_label.setStyleSheet("font-size: 15px; color: white; border: none;")
        
        h.addWidget(self.quiz_name_label)
        h.addWidget(self.subject_label)
        return header

    def _build_left(self):
        left = QVBoxLayout()
        left.setSpacing(10)

        card = QFrame()
        card.setStyleSheet(st.CARD_FRAME)
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(0, 0, 0, 20)
        card_lay.setSpacing(12)

        bar = QFrame()
        bar.setStyleSheet(st.HEADER_CONTAINER)
        bar.setFixedHeight(64)
        bar_lay = QHBoxLayout(bar)
        bar_lay.setContentsMargins(24, 10, 24, 10)

        self.q_type_label = QLabel("Multiple Choice")
        self.q_type_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white; border: none;")

        self.q_count_label = QLabel("Question 1 of 1")
        self.q_count_label.setStyleSheet("font-size: 14px; color: white; border: none;")

        bar_lay.addWidget(self.q_type_label)
        bar_lay.addStretch()
        bar_lay.addWidget(self.q_count_label)
        card_lay.addWidget(bar)

        self.q_title = QLabel("Question")
        self.q_title.setWordWrap(True)
        self.q_title.setStyleSheet(f"background: transparent; border: none; font-size: 28px; font-weight: bold; color: {st.Colors.TEXT_DARK};")

        q_wrap = QHBoxLayout()
        q_wrap.setContentsMargins(28, 0, 28, 0)
        q_wrap.addWidget(self.q_title)
        card_lay.addLayout(q_wrap)

        self.options_container = QWidget()
        self.options_container.setStyleSheet("border: none; background: transparent;")
        self.options_layout = QVBoxLayout(self.options_container)
        self.options_layout.setContentsMargins(28, 0, 28, 0)
        self.options_layout.setSpacing(12)

        self.button_group = QButtonGroup(self)
        self.button_group.idToggled.connect(self.on_option_selected)

        card_lay.addWidget(self.options_container)
        card_lay.addStretch()
        left.addWidget(card, 1)

        return left

    def _build_right(self):
        right = QVBoxLayout()
        right.setSpacing(18)

        navi = QFrame()
        navi.setStyleSheet(st.CARD_FRAME)
        navi.setFixedWidth(200)
        navi_lay = QVBoxLayout(navi)
        navi_lay.setContentsMargins(12, 16, 12, 12)
        navi_lay.setSpacing(6)
        
        title = QLabel("Quiz navigation")
        title.setStyleSheet(st.LABEL_SIDEBAR_HEADER)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        navi_lay.addWidget(title)

        holder = QWidget()
        holder.setAutoFillBackground(False)

        self.nav_list = QVBoxLayout(holder)
        self.nav_list.setContentsMargins(0, 0, 0, 0)
        self.nav_list.setSpacing(6)
        self.nav_list.setAlignment(Qt.AlignmentFlag.AlignTop)

        for idx in range(self.totalQuestions):
            item_btn = QPushButton(f"Question {idx + 1}")
            item_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            item_btn.clicked.connect(lambda _, q_idx=idx: self.goto_question(q_idx))
            self.nav_list.addWidget(item_btn)
            self.nav_buttons.append(item_btn)

        scroll = QScrollArea()
        scroll.setStyleSheet(st.SIDEBAR_SCROLL_AREA)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidget(holder)
        navi_lay.addWidget(scroll, 1)

        navi_lay.addStretch()
        right.addWidget(navi, 1)
        right.addSpacing(40)

        return right

    def _build_footer(self):
        footer = QHBoxLayout()
        footer.setContentsMargins(26, 0, 26, 18)
        
        self.btn_prev = QPushButton("Previous")
        self.btn_prev.setStyleSheet(st.BTN_SECONDARY)
        self.btn_prev.clicked.connect(self.prev_question)

        self.btn_next = QPushButton("Next")
        self.btn_next.setStyleSheet(st.BTN_PRIMARY)
        self.btn_next.clicked.connect(self.handle_next_or_submit)

        footer.addWidget(self.btn_prev)
        footer.addStretch()
        footer.addWidget(self.btn_next)
        return footer

    def display_question(self, index):
        q_data = self.questions[index]

        self.currentQuestion = index
        self.q_count_label.setText(f"Question {index + 1} of {self.totalQuestions}")
        self.q_type_label.setText(q_data["type"])
        self.q_title.setText(q_data["question"])

        for frame in self.option_frames:
            self.options_layout.removeWidget(frame)
            frame.deleteLater()
        self.option_frames.clear()

        for btn in self.button_group.buttons():
            self.button_group.removeButton(btn)

        for i, text in enumerate(q_data["options"]):
            opt_frame = QFrame()
            opt_layout = QHBoxLayout(opt_frame)
            opt_layout.setContentsMargins(12, 12, 12, 12)

            radio = QRadioButton(text)
            self.button_group.addButton(radio, i)

            is_selected = (self.user_answers.get(index) == i)
            radio.setChecked(is_selected)
            opt_frame.setStyleSheet(st.option_frame(is_selected))

            opt_layout.addWidget(radio)
            self.options_layout.addWidget(opt_frame)
            self.option_frames.append(opt_frame)

        self.btn_prev.setEnabled(index > 0)
        
        if index == self.totalQuestions - 1:
            self.btn_next.setText("Submit quiz")
        else:
            self.btn_next.setText("Next")
        self.btn_next.setEnabled(True)

        self.update_sidebar()

    def update_sidebar(self):
        for idx, btn in enumerate(self.nav_buttons):
            is_current = (idx == self.currentQuestion)
            is_answered = idx in self.user_answers

            if is_current:
                btn.setStyleSheet(st.nav_button("current"))
            elif is_answered:
                btn.setStyleSheet(st.nav_button("answered"))
            else:
                btn.setStyleSheet(st.nav_button("default"))

    def on_option_selected(self, option_id, checked):
        if checked:
            self.user_answers[self.currentQuestion] = option_id
            for idx, frame in enumerate(self.option_frames):
                frame.setStyleSheet(st.option_frame(idx == option_id))
            self.update_sidebar()

    def handle_next_or_submit(self):
        if self.currentQuestion == self.totalQuestions - 1:
            self.submit_quiz()
        else:
            self.next_question()

    def next_question(self):
        if self.currentQuestion < self.totalQuestions - 1:
            self.currentQuestion += 1
            self.display_question(self.currentQuestion)

    def prev_question(self):
        if self.currentQuestion > 0:
            self.currentQuestion -= 1
            self.display_question(self.currentQuestion)

    def goto_question(self, index):
        self.currentQuestion = index
        self.display_question(self.currentQuestion)

    def submit_quiz(self):
        unanswered = self.totalQuestions - len(self.user_answers)
        message = "Are you sure you want to submit your quiz?"
        if unanswered > 0:
            message = f"You have {unanswered} unanswered question(s).\n\nAre you sure you want to submit?"

        reply = QMessageBox.question(
            self, "Confirm Submission", message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        score = 0
        total_points = sum(q.get("points", 1) for q in self.questions)
        answers_export = {}

        for i, q in enumerate(self.questions):
            selected_idx = self.user_answers.get(i)
            selected_option = q["options"][selected_idx] if selected_idx is not None and selected_idx < len(q["options"]) else "None"
            is_correct = (selected_idx == q["correct_idx"])
            if is_correct:
                score += q.get("points", 1)

            answers_export[i] = {
                "question": q["question"],
                "selected_option": selected_option,
                "correct_option": q["correct"],
                "is_correct": is_correct
            }

        percentage = (score / total_points * 100) if total_points > 0 else 0.0
        save_student_result(self.username, self.quiz_id, score, total_points, percentage, answers_export)
        
        self.quiz_submitted.emit(self.username, self.quiz_id)
        self.close()
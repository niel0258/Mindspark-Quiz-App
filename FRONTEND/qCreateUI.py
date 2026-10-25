import sys
import csv
import re
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QButtonGroup, QComboBox, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSpinBox, QVBoxLayout, QWidget, QScrollArea, QMessageBox
)
from PyQt6.QtGui import QIcon, QValidator

from pathlib import Path
script_dir = Path(__file__).resolve().parent
backend_dir = Path(__file__).resolve().parent / ".." / "BACKEND"
sys.path.insert(0, str(backend_dir))

from question import MultipleChoice, TrueOrFalse
import styles as st
from database import save_quiz_to_db, initialize_quiz_storage, get_quiz_from_db, update_quiz_in_db

TYPE_NAMES = {
    "Multiple_Choice" : "Multiple Choice",
    "True_or_False" : "True or False"
}
TYPE_KEYS = {text:key for key,text in TYPE_NAMES.items()}
QUESTION_CLASSES  = {
    "Multiple_Choice" : MultipleChoice,
    "True_or_False" : TrueOrFalse
}

SUBJECTS = ["English", "Math", "Science", "Computer"]


def pill(text):
    b = QPushButton(text)
    b.setStyleSheet(st.BTN_PILL)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    return b

def round_btn(text="X"):
    b = QPushButton(text)
    b.setStyleSheet(st.BTN_ROUND_DELETE)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    return b

class UpperValidator(QValidator):
    def validate(self, text, pos):
        return QValidator.State.Acceptable, text[:1].upper() + text[1:], pos

class QuizEditor(QWidget):
    saved = pyqtSignal()
    def __init__(self, quiz_name="Quiz name", subject="English", username="teacher", quiz_id = None):
        super().__init__()
        self.quiz_id = quiz_id        
        self.setObjectName("root")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(st.MAIN_WINDOW)
        self.setWindowTitle(quiz_name)
        self.setWindowIcon(QIcon(str(script_dir / "logo.png")))
        self.resize(1280, 720)
        self.username = username

        self.option_edits = []
        self.option_radio = []
        self.option_containers = []
        self.option_group = QButtonGroup(self)
        self.option_group.idToggled.connect(self.on_option_toggled)
        self.maxOptions = 4
        self.qType = "Multiple_Choice"

        self.questions = []
        self.current = 0

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(self._build_header(quiz_name, subject))

        body = QHBoxLayout()
        body.setContentsMargins(26, 34, 26, 12)
        body.setSpacing(55)
        body.addLayout(self._build_left(), 1)
        body.addLayout(self._build_right())
        outer.addLayout(body, 1)
        outer.addLayout(self._build_footer())

        self.questions = [self.new_question("Multiple_Choice")]
        self.load_question(0)
        if quiz_id is not None:
            self.load_quiz(quiz_id)

    def add_option(self):
        if (len(self.option_edits) >= self.maxOptions):
            return
        self._add_option_row()
           
    def _add_option_row(self, text="", fixed=False):
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        
        container = QFrame()
        container.setLayout(row)
        
        select_btn = QRadioButton()
        select_btn.setToolTip("Set as correct option")
        select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.option_group.addButton(select_btn, len(self.option_edits))
        
        option_name = QLineEdit(text)
        option_name.setReadOnly(fixed)
        option_name.setStyleSheet(st.INPUT_FIELD)
        option_name.setPlaceholderText("Insert Option")
        option_name.setValidator(UpperValidator(self))
        option_name.editingFinished.connect(self.save_current_question)
        option_name.setCursor(Qt.CursorShape.IBeamCursor)
        
        self.option_edits.append(option_name)
        self.option_radio.append(select_btn)
        self.option_containers.append(container)
        
        row.addWidget(select_btn)
        row.addWidget(option_name, 1)

        if not fixed:
            rmv_btn = round_btn()
            row.addWidget(rmv_btn)
            rmv_btn.clicked.connect(lambda: self._deleteOption(container))

        is_selected = select_btn.isChecked()
        container.setStyleSheet(st.option_frame(is_selected))

        self.options_layout.addWidget(container)
        self._update_add_option_state()

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _deleteOption(self, container):
        if container in self.option_containers:
            index = self.option_containers.index(container)
            self.option_edits.pop(index)
            rad_btn = self.option_radio.pop(index)
            self.option_containers.pop(index)
            self.option_group.removeButton(rad_btn)

            for i, btn in enumerate(self.option_radio):
                self.option_group.setId(btn, i)

        self.options_layout.removeWidget(container)
        container.deleteLater() 
        self._update_add_option_state()

    def _clear_options(self):
        self._clear_layout(self.options_layout)
        self.option_edits = []
        self.option_radio = []
        self.option_containers = []
        old_group = self.option_group
        self.option_group = QButtonGroup(self)
        self.option_group.idToggled.connect(self.on_option_toggled)
        old_group.deleteLater()

    def _update_add_option_state(self):
        curr_q = self.questions[self.current]
        self.add_option_btn.setEnabled(curr_q.qType == "Multiple_Choice" and len(self.option_edits) < self.maxOptions)

    def on_option_toggled(self, option_id, checked):
        if 0 <= option_id < len(self.option_containers):
            self.option_containers[option_id].setStyleSheet(st.option_frame(checked))
        self.save_current_question()

    def _checked_index(self):
        for i, radio in enumerate(self.option_radio):
            if radio.isChecked():
                return i
        return None

    def new_question(self, qtype):
        q = QUESTION_CLASSES[qtype]()
        q.qType = qtype
        q.qTitle = self.quiz_name_edit.text()
        q.subj_name = self.subject_edit.currentText()
        return q
 
    def save_current_question(self):
        q = self.questions[self.current]
        q.qTitle = self.quiz_name_edit.text()
        q.subj_name = self.subject_edit.currentText()
        q.question = self.question_edit.text()
        q.points = self.points.value()
        if q.qType == "Multiple_Choice":
            q.choices = [e.text() for e in self.option_edits]
        q.right_answer = self._checked_index()

    def is_question_valid(self):
        q = self.questions[self.current]
        if not q.question.strip() or q.points < 0 or not q.choices:
            QMessageBox.warning(self, "Warning", "Fill in on the details before accessing a different question")
            return False
        return True
 
    def load_question(self, index):
        self.current = index
        q = self.questions[index]
        self.qType = q.qType
 
        self.combo.setCurrentIndex(self.combo.findText(TYPE_NAMES[q.qType]))
        self.question_edit.setText(q.question)
        self.points.setValue(q.points)
 
        self._clear_options()
        fixed = q.qType == "True_or_False"
        for text in q.choices:
            self._add_option_row(text, fixed)
        if isinstance(q.right_answer, int) and 0 <= q.right_answer < len(self.option_radio):
            self.option_radio[q.right_answer].setChecked(True)
            self.option_containers[q.right_answer].setStyleSheet(st.option_frame(True))
 
        self._update_add_option_state()
        self.refresh_nav()
        
    def load_quiz(self, quiz_id):
        data = get_quiz_from_db(quiz_id)
        if data is None:
            QMessageBox.warning(self, "Not found", "This quiz no longer exists.")
            return
        self.quiz_name_edit.setText(data["quiz_name"])
        if isinstance(self.subject_edit, QComboBox):
            idx = self.subject_edit.findText(data["subject"])
            self.subject_edit.setCurrentIndex(idx if idx >= 0 else 0)
        else:
            self.subject_edit.setText(data["subject"])

        self.questions = []
        for qd in data["questions"]:
            q = self.new_question(qd["qType"])
            q.question = qd["question"]
            q.points = qd["points"]
            q.choices = qd["choices"]
            q.right_answer = qd["right_answer"]
            self.questions.append(q)
        if not self.questions:
            self.questions = [self.new_question("Multiple_Choice")]
        self.load_question(0)
        self.setWindowTitle(f"Editing: {data['quiz_name']}")
 
    def add_question(self):
        self.save_current_question()
        self.questions.append(self.new_question("Multiple_Choice"))
        self.load_question(len(self.questions) - 1)
 
    def goto_question(self, index):
        if index != self.current:
            self.load_question(index)
        else:
            self.refresh_nav()
 
    def delete_question(self, index):
        self.save_current_question()
        if len(self.questions) == 1:
            self.questions[0] = self.new_question("Multiple_Choice")
            self.load_question(0)
            return
        del self.questions[index]
        if index < self.current:
            self.current -= 1
        self.current = min(self.current, len(self.questions) - 1)
        self.load_question(self.current)
 
    def on_type_changed(self, text):
        new_type = TYPE_KEYS[text]
        old = self.questions[self.current]
        if new_type == old.qType:
            return
        self.save_current_question()
        new = self.new_question(new_type)
        new.question = old.question
        new.points = old.points
        self.questions[self.current] = new
        self.load_question(self.current)
 
    def refresh_nav(self):
        self._clear_layout(self.nav_list)
        for i in range(len(self.questions)):
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            
            is_current = (i == self.current)
            item = QPushButton(f"Question {i + 1}")
            item.setStyleSheet(st.nav_button("current" if is_current else "default"))
            item.setCheckable(True)
            item.setChecked(is_current)
            item.setCursor(Qt.CursorShape.PointingHandCursor)
            item.clicked.connect(lambda _, idx=i: self.goto_question(idx))
            
            delete = round_btn()
            delete.clicked.connect(lambda _, idx=i: self.delete_question(idx))
            
            row.addWidget(item, 1)
            row.addWidget(delete)
            container = QWidget()
            container.setLayout(row)
            self.nav_list.addWidget(container)

    def _build_header(self, quiz_name, subject):
        header = QFrame()
        header.setStyleSheet(st.HEADER_CONTAINER)
        header.setFixedHeight(95)
        h = QVBoxLayout(header)
        h.setContentsMargins(48, 8, 20, 8)
        h.setSpacing(4)
        
        row1 = QHBoxLayout()
        row1.setContentsMargins(0, 0, 0, 0)
        lbl_q = QLabel("Quiz Name:")
        lbl_q.setStyleSheet("color: white; font-weight: bold;")
        self.quiz_name_edit = QLineEdit(quiz_name)
        self.quiz_name_edit.setStyleSheet(st.INPUT_FIELD)
        self.quiz_name_edit.editingFinished.connect(self.save_current_question)
        row1.addWidget(lbl_q)
        row1.addWidget(self.quiz_name_edit, 1)

        row2 = QHBoxLayout()
        row2.setContentsMargins(0, 0, 0, 0)
        lbl_s = QLabel("Course/Subject:")
        lbl_s.setStyleSheet("color: white; font-weight: bold;")
        self.subject_edit = QComboBox()
        self.subject_edit.addItems(SUBJECTS)
        self.subject_edit.setStyleSheet(st.COMBOBOX)
        idx = self.subject_edit.findText(subject)
        self.subject_edit.setCurrentIndex(idx if idx >=0 else 0)
        self.subject_edit.currentTextChanged.connect(self.save_current_question)
        row2.addWidget(lbl_s)
        row2.addWidget(self.subject_edit, 1)

        h.addLayout(row1)
        h.addLayout(row2)
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

        self.combo = QComboBox()
        self.combo.setStyleSheet(st.COMBOBOX)
        self.combo.addItem("Multiple Choice")
        self.combo.addItem("True or False")
        self.combo.setMinimumWidth(350)
        self.combo.currentTextChanged.connect(self.on_type_changed)
        
        self.points = QSpinBox()
        self.points.setStyleSheet(st.SPINBOX)
        self.points.setRange(0, 1000)
        self.points.setSuffix(" points")
        self.points.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.points.setAlignment(Qt.AlignmentFlag.AlignRight)

        bar_lay.addWidget(self.combo)
        bar_lay.addStretch()
        bar_lay.addWidget(self.points)
        card_lay.addWidget(bar)

        self.question_edit = QLineEdit()
        self.question_edit.setStyleSheet(f"QLineEdit {{ background: transparent; border: none; font-size: 28px; font-weight: bold; color: {st.Colors.TEXT_DARK}; }}")
        self.question_edit.setPlaceholderText("Insert Question")
        self.question_edit.setValidator(UpperValidator(self))
        self.question_edit.editingFinished.connect(self.save_current_question)

        q_wrap = QHBoxLayout()
        q_wrap.setContentsMargins(28, 0, 28, 0)
        q_wrap.addWidget(self.question_edit)
        card_lay.addLayout(q_wrap)

        self.options_layout = QVBoxLayout()
        self.options_layout.setContentsMargins(28, 0, 28, 0)
        self.options_layout.setSpacing(12)
        card_lay.addLayout(self.options_layout)

        add_row = QHBoxLayout()
        add_row.setContentsMargins(28, 0, 28, 0)
        self.add_option_btn = pill("Add Option")
        add_row.addSpacing(10)
        add_row.addWidget(self.add_option_btn, 1)
        self.add_option_btn.clicked.connect(self.add_option)
        card_lay.addLayout(add_row)
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

        scroll = QScrollArea()
        scroll.setStyleSheet(st.SIDEBAR_SCROLL_AREA)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidget(holder)
        navi_lay.addWidget(scroll, 1)   

        navi_lay.addStretch()
        right.addWidget(navi, 1)

        self.add_question_btn = pill("Add question")
        self.add_question_btn.clicked.connect(self.add_question)
        right.addWidget(self.add_question_btn)
        right.addSpacing(40)
        return right

    def _build_footer(self):
        footer = QHBoxLayout()
        footer.setContentsMargins(26, 0, 26, 18)
        footer.addStretch()
        self.finish_btn = pill("FINISH & SAVE")
        self.finish_btn.clicked.connect(self.finish_and_export)
        footer.addWidget(self.finish_btn)
        return footer

    def finish_and_export(self):
        self.save_current_question()
        quiz_name = self.quiz_name_edit.text().strip()
        subject_name = self.subject_edit.currentText().strip()

        if not quiz_name or not subject_name:
            QMessageBox.warning(self, "Warning", "Please provide a Quiz Name and Subject/Course.")
            return

        for i, q in enumerate(self.questions):
            if not q.question.strip() or q.right_answer is None:
                QMessageBox.warning(self, "Incomplete Question", f"Question {i+1} is missing text or a correct option.")
                return

        questions_data = []
        for q in self.questions:
            questions_data.append({
                "qType": q.qType,
                "question": q.question,
                "points": q.points,
                "choices": q.choices,
                "right_answer": q.right_answer
            })

        initialize_quiz_storage()
        if self.quiz_id is None:
            success = save_quiz_to_db(quiz_name, subject_name, self.username, questions_data)
        else:
            success = update_quiz_in_db(self.quiz_id, quiz_name, subject_name, questions_data)
        if success:
            QMessageBox.information(self, "Success", "Quiz Saved successfully")
            self.saved.emit()
            self.close()
            """
            default_filename = re.sub(r'[\\/*?:"<>|]', "", f"{quiz_name}_{subject_name}").strip().replace(" ", "_") + ".csv"
            file_path, _ = QFileDialog.getSaveFileName(self, "Export Quiz to CSV", default_filename, "CSV Files (*.csv)")
            if file_path:
                try:
                    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(["Quiz Title", "Subject Name", "Question Type", "Question", "Option 1", "Option 2", "Option 3", "Option 4", "Correct Option", "Points"])
                        for q in self.questions:
                            opts = q.choices + [""] * (4 - len(q.choices))
                            correct_val = q.choices[q.right_answer] if q.right_answer is not None and q.right_answer < len(q.choices) else ""
                            writer.writerow([quiz_name, subject_name, q.qType, q.question, opts[0], opts[1], opts[2], opts[3], correct_val, q.points])
                    QMessageBox.information(self, "Success", "Quiz saved to database and exported to CSV successfully!")
                    self.close()
                except Exception as e:
                    QMessageBox.critical(self, "Export Error", f"Failed to export CSV: {e}")
                    """
        else:
            QMessageBox.critical(self, "Database Error", "Failed to save quiz to database.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = QuizEditor("Quiz name", "Subject name", "teacher")
    view.show()
    sys.exit(app.exec())

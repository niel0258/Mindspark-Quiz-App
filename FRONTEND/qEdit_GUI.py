import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QButtonGroup, QComboBox, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSpinBox, QVBoxLayout, QWidget,
)

from question import MultipleChoice,TrueOrFalse

#-----------------------------------------------------------------------------
# Question types
#----------------------------------------------------------------------------

TYPE_NAMES = {
    "Multiple_Choice" : "Multiple Choice",
    "True_or_False" : "True or False"
}
TYPE_KEYS = {text:key for key,text in TYPE_NAMES.items()}
QUESTION_CLASSES  = {
    "Multiple_Choice" : MultipleChoice,
    "True_or_False" : TrueOrFalse
}

# ---------------------------------------------------------------------------
# Theme colors
# ---------------------------------------------------------------------------
MAROON = "#651416"
RED = "#ff2a2a"

STYLE = f"""
#root {{ background: white; }}

#header {{ background: {MAROON}; }}
#quizName {{ font-size: 26px; font-weight: bold; color: white; }}
#subjectName {{ font-size: 15px; color: white; }}

#card {{ background: #d9d9d9; border-radius: 28px; }}

#cardBar {{ background: {MAROON}; border-radius: 28px; }}
#cardBar QComboBox {{
    background: transparent; color: white; border: none;
    font-size: 18px; font-weight: bold; padding: 4px 8px;
}}
#cardBar QComboBox::drop-down {{ border: none; width: 24px; }}
#cardBar QComboBox QAbstractItemView {{
    background: white; color: black; selection-background-color: {MAROON};
    selection-color: white; font-size: 14px; font-weight: normal;
}}
#cardBar QSpinBox {{
    background: transparent; color: white; border: none; font-size: 14px;
}}

#option{{
    background: white; color: black; border: none;
    border-radius: 15px; padding: 9px 20px; font-size: 14px;
}}

#questionEdit {{
    background: transparent; border: none;
    font-size: 28px; font-weight: bold;
}}
#optionEdit {{
    background: white; border: none; border-radius: 13px;
    padding: 6px 14px; font-size: 14px;
}}

QRadioButton::indicator {{
    width: 26px; height: 26px; border-radius: 15px;
    border: 2px solid {MAROON}; background: white;
}}
QRadioButton::indicator:checked {{
    background: qradialgradient(cx:.5, cy:.5, radius:.5, fx:.5, fy:.5,
        stop:0 {MAROON}, stop:0.5 {MAROON}, stop:0.55 white, stop:1 white);
}}

#navi {{ background: #ebebeb; border-radius: 28px; }}
#naviTitle {{
    background: {MAROON}; color: white; border-radius: 26px;
    font-size: 14px; font-weight: bold; min-height: 52px; max-height: 52px;
}}
#navi QPushButton#navItem {{              /* clickable question name */
    background: transparent; color: black; border: none;
    font-size: 15px; text-align: left; padding: 4px;
}}
#navi QPushButton#navItem:checked {{ font-weight: bold; }}  /* current question */

QPushButton#pill {{
    background: {MAROON}; color: white; border: none;
    border-radius: 15px; padding: 9px 20px; font-size: 14px;
}}
QPushButton#pill:disabled {{ background: #9b7a7b; }}
QPushButton#addOption {{
    background: white; color: black; border: none;
    border-radius: 15px; padding: 9px 20px; font-size: 14px;
}}
QPushButton#round {{
    background: {RED}; color: white; border: none; border-radius: 17px;
    min-width: 34px; max-width: 34px; min-height: 34px; max-height: 34px;
}}
"""

def pill(text, name="pill"):
    b = QPushButton(text)
    b.setObjectName(name)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    return b


def round_btn(text="X"):
    b = QPushButton(text)
    b.setObjectName("round")
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    return b


def clear_layout(layout):
   #Remove and delete every widget inside a layout.
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()

class QuizEditor(QWidget):
    def __init__(self, quiz_name="Quiz name", subject="Subject name"):
        super().__init__()
        self.setObjectName("root")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setWindowTitle(quiz_name)
        self.resize(1280, 720)

        # Option rows are rebuilt often; keep references to the current ones
        self.option_edits = []
        self.option_radio = []
        self.option_group = QButtonGroup(self)
        self.maxOptions = 4
        self.qType = "Multiple_Choice"

        #question tracking
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

        self.setStyleSheet(STYLE)

        self.questions = [self.new_question("Multiple_Choice")]
        self.load_question(0)

    #Connected options
    def add_option(self):
        if (len(self.option_edits) >= self.maxOptions):
            return
        self._add_option_row()
           
    def _add_option_row(self,text = "",fixed = False):
        row = QHBoxLayout()
        row.setContentsMargins(0,0,0,0)
        select_btn = QRadioButton()
        select_btn.setToolTip("Set as correct option")
        select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.option_group.addButton(select_btn)
        #add function that sets it correct
        option_name = QLineEdit(text)
        option_name.setReadOnly(fixed)
        option_name.setObjectName("option")
        option_name.setPlaceholderText("Insert Option")
        #call a event when name is changed
        option_name.setCursor(Qt.CursorShape.IBeamCursor)
        self.option_edits.append(option_name)
        self.option_radio.append(select_btn)
        
        row.addWidget(select_btn)
        row.addWidget(option_name,1)

        if not fixed:
            rmv_btn = round_btn()
            row.addWidget(rmv_btn)
            rmv_btn.clicked.connect(lambda: self._deleteOption(container))

        container = QWidget()
        container.setLayout(row)

        self.options_layout.addWidget(container)

        self._update_add_option_state()

    def _deleteOption(self,container):
        lineEdit = container.findChild(QLineEdit)

        if lineEdit in self.option_edits:
            index = self.option_edits.index(lineEdit)
            self.option_edits.pop(index)
            rad_btn = self.option_radio.pop(index)
            self.option_group.removeButton(rad_btn)

        self.options_layout.removeWidget(container)
        container.deleteLater() 
        self._update_add_option_state()

    def _clear_options(self):
        clear_layout(self.options_layout)
        self.option_edits = []
        self.option_radio = []
        old_group = self.option_group #store to another variable to prevent leaks
        self.option_group = QButtonGroup(self)
        old_group.deleteLater()

    def _update_add_option_state(self):
        curr_q = self.questions[self.current]
        self.add_option_btn.setEnabled(curr_q.qType == "Multiple_Choice" and len(self.option_edits) < self.maxOptions)

    def _checked_index(self):
        for i,radio in enumerate(self.option_radio):
            if radio.isChecked():
                return i
        return None

    #add questions and remove
    def new_question(self, qtype):
        q = QUESTION_CLASSES[qtype]()
        q.qType = qtype
        q.qTitle = self.quiz_name_label.text()
        q.subj_name = self.subject_label.text()
        return q
 
    def save_current_question(self):
        q = self.questions[self.current]
        q.qTitle = self.quiz_name_label.text()
        q.subj_name = self.subject_label.text()
        q.question = self.question_edit.text()
        q.points = self.points.value()
        if q.qType == "Multiple_Choice":
            q.choices = [e.text() for e in self.option_edits]
        q.right_answer = self._checked_index()
 
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
            self._add_option_row(text,fixed)
        if isinstance(q.right_answer, int) and 0 <= q.right_answer < len(self.option_radio):
            self.option_radio[q.right_answer].setChecked(True)
 
        self._update_add_option_state()
        self.refresh_nav()
 
    def add_question(self):
        self.save_current_question()
        self.questions.append(self.new_question("Multiple_Choice"))
        self.load_question(len(self.questions) - 1)
 
    def goto_question(self, index):
        if index != self.current:
            self.save_current_question()
            self.load_question(index)
        else:
            self.refresh_nav()  # a click toggles the button; redraw to restore it
 
    def delete_question(self, index):
        self.save_current_question()
        if len(self.questions) == 1:
            # a quiz keeps at least one question: reset it instead
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
        new.question = old.question       # keep the text and points,
        new.points = old.points           # choices don't carry over
        self.questions[self.current] = new
        self.load_question(self.current)
 
    def refresh_nav(self):
        clear_layout(self.nav_list)
        for i in range(len(self.questions)):
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            item = QPushButton(f"question {i + 1}")
            item.setObjectName("navItem")
            item.setCheckable(True)
            item.setChecked(i == self.current)
            item.setCursor(Qt.CursorShape.PointingHandCursor)
            item.clicked.connect(lambda _=False, idx=i: self.goto_question(idx))
            delete = round_btn()
            delete.clicked.connect(lambda _=False, idx=i: self.delete_question(idx))
            row.addWidget(item, 1)
            row.addWidget(delete)
            container = QWidget()
            container.setLayout(row)
            self.nav_list.addWidget(container)

    
    # =======================================================================
    # UI CONSTRUCTION
    # =======================================================================
    def _build_header(self, quiz_name, subject):
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(82)
        h = QVBoxLayout(header)
        h.setContentsMargins(48, 8, 20, 8)
        h.setSpacing(0)
        self.quiz_name_label = QLabel(quiz_name)
        self.quiz_name_label.setObjectName("quizName")
        self.subject_label = QLabel(subject)
        self.subject_label.setObjectName("subjectName")
        h.addWidget(self.quiz_name_label)
        h.addWidget(self.subject_label)
        return header

    def _build_left(self):
        left = QVBoxLayout()
        left.setSpacing(10)

        card = QFrame()
        card.setObjectName("card")
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(0, 0, 0, 20)
        card_lay.setSpacing(12)

        # top bar: question picker + points
        bar = QFrame()
        bar.setObjectName("cardBar")
        bar.setFixedHeight(64)
        bar_lay = QHBoxLayout(bar)
        bar_lay.setContentsMargins(24, 10, 24, 10)
        self.combo = QComboBox()
        self.combo.setObjectName("qTSelect")
        self.combo.addItem("Multiple Choice")
        self.combo.addItem("True or False")
        self.combo.setMinimumWidth(350)
        self.combo.currentTextChanged.connect(self.on_type_changed)
        self.points = QSpinBox()
        self.points.setRange(0, 1000)
        self.points.setSuffix(" points")
        self.points.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.points.setAlignment(Qt.AlignmentFlag.AlignRight)
        bar_lay.addWidget(self.combo)
        bar_lay.addStretch()
        bar_lay.addWidget(self.points)
        card_lay.addWidget(bar)

        # question text
        self.question_edit = QLineEdit()
        self.question_edit.setObjectName("questionEdit")
        self.question_edit.setPlaceholderText("Insert Question")
        q_wrap = QHBoxLayout()
        q_wrap.setContentsMargins(28, 0, 28, 0)
        q_wrap.addWidget(self.question_edit)
        card_lay.addLayout(q_wrap)

        # option rows live here (filled by set_options)
        self.options_layout = QVBoxLayout()
        self.options_layout.setContentsMargins(28, 0, 28, 0)
        self.options_layout.setSpacing(12)
        card_lay.addLayout(self.options_layout)

        # "Add Option" row, always right below the last option
        add_row = QHBoxLayout()
        add_row.setContentsMargins(28, 0, 28, 0)
        self.add_option_btn = pill("Add Option", "addOption")
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
        navi.setObjectName("navi")
        navi.setFixedWidth(200)
        navi_lay = QVBoxLayout(navi)
        navi_lay.setContentsMargins(0, 0, 0, 12)
        navi_lay.setSpacing(6)
        title = QLabel("Quiz Navi")
        title.setObjectName("naviTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        navi_lay.addWidget(title)

        # question rows live here (filled by set_questions)
        self.nav_list = QVBoxLayout()
        self.nav_list.setContentsMargins(14, 0, 8, 0)
        self.nav_list.setSpacing(6)
        navi_lay.addLayout(self.nav_list)
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
        self.finish_btn = pill("FINISH")
        footer.addWidget(self.finish_btn)
        return footer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = QuizEditor("Quiz name", "Subject name")
    view.show()
    sys.exit(app.exec())
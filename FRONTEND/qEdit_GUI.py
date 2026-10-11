import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QButtonGroup, QComboBox, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSpinBox, QVBoxLayout, QWidget,
)

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
        self.option_group = QButtonGroup(self)
        self.qType = "Multiple_Choice"

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

    #Connected options
    def add_option(self):
        row = QHBoxLayout()
        row.setContentsMargins(0,0,0,0)
        select_btn = QRadioButton()
        select_btn.setToolTip("Set as correct option")
        self.option_group.addButton(select_btn,len(self.option_edits) - 1)
        #add function that sets it correct
        option_name = QLineEdit()
        option_name.setObjectName("navItem")
        option_name.setPlaceholderText("Insert Option")
        #call a event when name is changed
        option_name.setCursor(Qt.CursorShape.PointingHandCursor)
        self.option_edits.append(option_name)
        rmv_btn = round_btn()
        #add delete cll
        row.addWidget(select_btn)
        row.addWidget(option_name,1)
        row.addWidget(rmv_btn)

        container = QWidget()
        container.setLayout(row)

        self.options_layout.addWidget(container)

        if (len(self.option_edits) == 4):
            self.add_option_btn.setEnabled(False)

    def deleteOption(self):
        pass
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
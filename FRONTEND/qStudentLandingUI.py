import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QComboBox, QFrame
)

from pathlib import Path
backend_dir = Path(__file__).resolve().parent / ".." / "BACKEND"
sys.path.insert(0, str(backend_dir))

import styles as st
from database import get_all_quizzes

WINDOW_SIZE = (1280, 720)

TRANSLATIONS = {
    "English": {
        "home": "Home",
        "quizzes": "Quizzes",
        "quizzes_sub": "Quizzes to Take",
        "title": "Think\nDifferent.",
        "desc": "THIS IS AN ONLINE QUIZ PLATFORM GUI-BASED DIGITAL TOOL THAT LETS STUDENTS TAKE ENGAGING QUIZZES, RETAIN INFORMATION AND BOOST PARTICIPATION.",
        "play": "Let's Play",
        "sign_out": "Sign Out"
    },
    "Español": {
        "home": "Inicio",
        "quizzes": "Quizzes",
        "quizzes_sub": "Quizzes para Tomar",
        "title": "Piensa\nDiferente.",
        "desc": "ESTA ES UNA HERRAMIENTA DIGITAL BASADA EN GUI DE PLATAFORMA DE QUIZ EN LÍNEA QUE PERMITE A LOS ESTUDIANTES REALIZAR QUIZZES ATRACTIVOS.",
        "play": "Vamos a Jugar",
        "sign_out": "Cerrar Sesión"
    },
    "Filipino": {
        "home": "Tahanan",
        "quizzes": "Mga Pagsusulit",
        "quizzes_sub": "Mga Pagsusulit na Tatanawin",
        "title": "Mag-isip\nng Naiiba.",
        "desc": "ITO AY ISANG ONLINE QUIZ PLATFORM GUI-BASED DIGITAL TOOL NA NAGBIBIGAY-DAAN SA MGA MAG-AARAL NA KUMUHA NG MGA PAGSUSULIT.",
        "play": "Laro Tayo!",
        "sign_out": "Mag-sign Out"
    }
}

class StudentQuizLandingUI(QWidget):
    def __init__(self, username="student"):
        super().__init__()
        self.setWindowTitle("Student Quiz Platform")
        self.setFixedSize(*WINDOW_SIZE)
        self.username = username
        
        self.setObjectName("mainContainer")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            QWidget#mainContainer { background-color: #551515; }
        """)
        
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        
        top_ribbon = QFrame()
        top_ribbon.setStyleSheet("background-color: #3B0A0A; border: none;")
        top_ribbon_layout = QHBoxLayout(top_ribbon)
        top_ribbon_layout.setContentsMargins(30, 8, 30, 8)
        
        self.lang_dropdown = QComboBox()
        self.lang_dropdown.setStyleSheet(st.COMBOBOX)
        self.lang_dropdown.addItems(["Language ▾", "English", "Español", "Filipino"])
        self.lang_dropdown.currentTextChanged.connect(self.update_language)
        top_ribbon_layout.addWidget(self.lang_dropdown)
        
        top_ribbon_layout.addStretch()
        
        self.sign_out_btn = QPushButton("Sign Out")
        self.sign_out_btn.setStyleSheet(st.BTN_PRIMARY)
        top_ribbon_layout.addWidget(self.sign_out_btn)
        root_layout.addWidget(top_ribbon)
        
        nav_bar = QFrame()
        nav_bar.setStyleSheet("background-color: #2D0707; border: none;")
        nav_bar_layout = QHBoxLayout(nav_bar)
        nav_bar_layout.setContentsMargins(30, 15, 30, 15)
        
        brand_logo = QLabel("Student Portal")
        brand_logo.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF; background: transparent;")
        nav_bar_layout.addWidget(brand_logo)
        nav_bar_layout.addStretch()
        
        self.nav_home = QPushButton("Home")
        self.nav_home.setStyleSheet(st.BTN_SECONDARY)
        self.nav_quizzes = QPushButton("Quizzes")
        self.nav_quizzes.setStyleSheet(st.BTN_SECONDARY)
        self.nav_quizzes.clicked.connect(self.load_quizzes_view)
        self.nav_home.clicked.connect(self.reset_home_view)
        
        nav_bar_layout.addWidget(self.nav_home)
        nav_bar_layout.addWidget(self.nav_quizzes)
        root_layout.addWidget(nav_bar)
        
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(50, 50, 50, 40)
        body_layout.setSpacing(40)
        
        left_hero_block = QVBoxLayout()
        left_hero_block.setSpacing(15)
        left_hero_block.addStretch()
        
        self.quizzes_sub_label = QLabel("Quizzes to Take")
        self.quizzes_sub_label.setStyleSheet("color: #ca8a04; font-size: 12px; font-weight: bold; background: transparent;")
        left_hero_block.addWidget(self.quizzes_sub_label)
        
        self.hero_title = QLabel("Think\nDifferent.")
        self.hero_title.setStyleSheet("font-size: 64px; font-weight: 900; color: #FFFFFF; background: transparent; line-height: 1.1;")
        left_hero_block.addWidget(self.hero_title)
        
        self.hero_desc = QLabel("THIS IS AN ONLINE QUIZ PLATFORM GUI-BASED DIGITAL TOOL THAT LETS STUDENTS TAKE ENGAGING QUIZZES.")
        self.hero_desc.setStyleSheet("color: #E2C2C2; font-size: 13px; font-weight: bold; background: transparent;")
        self.hero_desc.setWordWrap(True)
        left_hero_block.addWidget(self.hero_desc)
        left_hero_block.addSpacing(10)
        
        cta_row = QHBoxLayout()
        cta_row.setSpacing(15)
        
        self.play_btn = QPushButton("Let's Play")
        self.play_btn.setStyleSheet(st.BTN_PILL)
        cta_row.addWidget(self.play_btn)
        cta_row.addStretch()
        
        left_hero_block.addLayout(cta_row)
        left_hero_block.addStretch()
        body_layout.addLayout(left_hero_block, stretch=30)
        
        graphic_container = QFrame()
        graphic_container.setStyleSheet("background: transparent; border: none;")
        graphic_layout = QVBoxLayout(graphic_container)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "dice.png")
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            transform = QTransform().rotate(15)
            scaled_pixmap = pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation).scaled(
                500, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText("[ Graphic Placeholder ]")
            self.image_label.setStyleSheet(st.LABEL_MUTED)
            
        graphic_layout.addWidget(self.image_label)
        body_layout.addWidget(graphic_container, stretch=4)
        root_layout.addLayout(body_layout)

    def load_quizzes_view(self):
        self.hero_title.setText("Quizzes to Take")
        quizzes = get_all_quizzes()
        if quizzes:
            desc_text = "\n".join([f"• Quiz ID {q[0]}: {q[1]} ({q[2]})" for q in quizzes])
        else:
            desc_text = "No quizzes available to take."
        self.hero_desc.setText(desc_text)

    def reset_home_view(self):
        self.hero_title.setText("Think\nDifferent.")
        self.hero_desc.setText("THIS IS AN ONLINE QUIZ PLATFORM GUI-BASED DIGITAL TOOL THAT LETS STUDENTS TAKE ENGAGING QUIZZES.")

    def update_language(self, language_name: str):
        lang_data = TRANSLATIONS.get(language_name)
        if not lang_data:
            return
        self.nav_home.setText(lang_data["home"])
        self.nav_quizzes.setText(lang_data["quizzes"])
        self.quizzes_sub_label.setText(lang_data["quizzes_sub"])
        self.hero_title.setText(lang_data["title"])
        self.hero_desc.setText(lang_data["desc"])
        self.play_btn.setText(lang_data["play"])
        self.sign_out_btn.setText(lang_data["sign_out"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = StudentQuizLandingUI()
    ui.show()
    sys.exit(app.exec())
import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap, QTransform
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QFrame,
)

WINDOW_SIZE = (980, 600)

# 1. Define translation dictionary mappings
TRANSLATIONS = {
    "English": {
        "home": "Home",
        "templates": "Templates",
        "quizzes": "My Quizzes",
        "title": "Think\nDifferent.",
        "desc": "THIS IS AN ONLINE QUIZ PLATFORM GUI-BASED DIGITAL TOOL THAT LETS STUDENTS AND EDUCATORS CREATE ENGAGING QUIZZES, RETAIN INFORMATION AND BOOST TRAINING PARTICIPATION.",
        "play": "Let's Play",
        "create": "Create Quiz",
        "sign_out": "Sign Out"
    },
    "Español": {
        "home": "Inicio",
        "templates": "Plantillas",
        "quizzes": "Mis Quizzes",
        "title": "Piensa\nDiferente.",
        "desc": "ESTA ES UNA HERRAMIENTA DIGITAL BASADA EN GUI DE PLATAFORMA DE QUIZ EN LÍNEA QUE PERMITE A ESTUDIANTES Y EDUCADORES CREAR QUIZZES ATRACTIVOS.",
        "play": "Vamos a Jugar",
        "create": "Crear Quiz",
        "sign_out": "Cerrar Sesión"
    },
    "Filipino": {
        "home": "Tahanan",
        "templates": "Mga Template",
        "quizzes": "Aking Pagsusulit",
        "title": "Mag-isip\nng Naiiba.",
        "desc": "ITO AY ISANG ONLINE QUIZ PLATFORM GUI-BASED DIGITAL TOOL NA NAGBIBIGAY-DAAN SA MGA MAG-AARAL AT GURO NA GUMAWA NG MGA PAGSUSULIT.",
        "play": "Laro Tayo!",
        "create": "Gumawa ng Pagsusulit",
        "sign_out": "Mag-sign Out"
    }
}

def _page_style() -> str:
    return """
    QWidget#mainContainer { 
        background-color: #551515; 
        }
    
    QFrame#topUtilityBar { 
        background-color: #3B0A0A; 
        border: none; 
        }

    QFrame#navBar { 
        background-color: #2D0707; 
        border: none; 
        }

    QLabel { 
        font-family: 'Segoe UI', Arial, sans-serif; color: #FFFFFF; 
        }
    
    QLabel#brandLogo { 
        font-size: 24px; 
        font-weight: bold; 
        padding-left: 30px; 
        }

    QLabel#heroTitle { 
        font-size: 80px; 
        font-weight: 900; 
        line-height: 1.1; 
        }

    QLabel#heroDescription { 
        font-size: 13px; 
        font-weight: bold; 
        color: #E2C2C2; 
        line-height: 1.4; 
        }

    QPushButton#navLink { 
        background: transparent; 
        border: none; 
        color: #FFFFFF; 
        font-size: 15px; 
        font-weight: 500; 
        padding: 5px 15px; 
        }

    QPushButton#navLink:hover { 
        color: #FFC800; 
        }

    QComboBox#languageDropdown { 
        background-color: #FFA500; 
        color: #3B0A0A; 
        border: none; 
        border-radius: 12px; 
        padding: 4px 12px; 
        font-weight: bold; 
        font-size: 13px; 
        }

    QComboBox#languageDropdown::drop-down { 
        border: none; 
        }
    
    QPushButton#utilityBtn { 
        background-color: #FFA500; 
        color: #3B0A0A; 
        border: none;
        border-radius: 12px; 
        padding: 6px 18px; 
        font-weight: bold; 
        font-size: 13px; 
        }

    QPushButton#actionBtn { 
        background-color: #FFA500; 
        color: #3B0A0A; 
        border: none; 
        border-radius: 18px; 
        font-size: 16px; 
        font-weight: bold; 
        min-height: 36px; 
        padding: 0px 24px; 
        }

    QPushButton#utilityBtn:hover, QPushButton#actionBtn:hover, QComboBox#languageDropdown:hover { 
        background-color: #FFB732; 
        }
        
    QFrame#graphicPlaceholder { 
        background-color: transparent; 
        border: none; 
    }
    """

class QuizLandingUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Landing Page")
        self.setFixedSize(*WINDOW_SIZE)
        
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        
        self.setObjectName("mainContainer")
        self.setStyleSheet(_page_style())
        
        # 1. Top Utility Ribbon Bar
        top_ribbon = QFrame()
        top_ribbon.setObjectName("topUtilityBar")
        top_ribbon_layout = QHBoxLayout(top_ribbon)
        top_ribbon_layout.setContentsMargins(30, 8, 30, 8)
        
        # Language Selector configuration
        self.lang_dropdown = QComboBox()
        self.lang_dropdown.setObjectName("languageDropdown")
        self.lang_dropdown.addItems(["Language ▾","English", "Español", "Filipino"])
        # Connect change event signal
        self.lang_dropdown.currentTextChanged.connect(self.update_language)
        top_ribbon_layout.addWidget(self.lang_dropdown)
        
        top_ribbon_layout.addStretch()
        
        self.sign_out_btn = QPushButton()
        self.sign_out_btn.setObjectName("utilityBtn")
        top_ribbon_layout.addWidget(self.sign_out_btn)
        root_layout.addWidget(top_ribbon)
        
        # 2. Navigation Header Bar
        nav_bar = QFrame()
        nav_bar.setObjectName("navBar")
        nav_bar_layout = QHBoxLayout(nav_bar)
        nav_bar_layout.setContentsMargins(10, 15, 30, 15)
        
        brand_logo = QLabel("name haha")
        brand_logo.setObjectName("brandLogo")
        nav_bar_layout.addWidget(brand_logo)
        nav_bar_layout.addStretch()
        
        # Core Navigation menu references
        self.nav_home = QPushButton()
        self.nav_home.setObjectName("navLink")
        self.nav_templates = QPushButton()
        self.nav_templates.setObjectName("navLink")
        self.nav_quizzes = QPushButton()
        self.nav_quizzes.setObjectName("navLink")
        
        nav_bar_layout.addWidget(self.nav_home)
        nav_bar_layout.addWidget(self.nav_templates)
        nav_bar_layout.addWidget(self.nav_quizzes)
        root_layout.addWidget(nav_bar)
        
        # 3. Main Hero Split Screen Zone
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(50, 50, 50, 40)
        body_layout.setSpacing(40)
        
        left_hero_block = QVBoxLayout()
        left_hero_block.setSpacing(15)
        left_hero_block.addStretch()
        
        self.hero_title = QLabel()
        self.hero_title.setObjectName("heroTitle")
        left_hero_block.addWidget(self.hero_title)
        
        self.hero_desc = QLabel()
        self.hero_desc.setObjectName("heroDescription")
        self.hero_desc.setWordWrap(True)
        left_hero_block.addWidget(self.hero_desc)
        left_hero_block.addSpacing(10)
        
        cta_row = QHBoxLayout()
        cta_row.setSpacing(15)
        
        self.play_btn = QPushButton()
        self.play_btn.setObjectName("actionBtn")
        self.create_btn = QPushButton()
        self.create_btn.setObjectName("actionBtn")
        
        cta_row.addWidget(self.play_btn)
        cta_row.addWidget(self.create_btn)
        cta_row.addStretch()
        
        left_hero_block.addLayout(cta_row)
        left_hero_block.addStretch()
        body_layout.addLayout(left_hero_block, stretch=30)
        
        # Right Graphic Asset Section Placeholder
        graphic_container = QFrame()
        graphic_container.setObjectName("graphicPlaceholder")
        
        graphic_layout = QVBoxLayout(graphic_container)
        graphic_layout.setContentsMargins(10, 10, 10, 10)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Absolute path mapping setup
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "dice.png")
        
        pixmap = QPixmap(image_path)
        
        if not pixmap.isNull():
            transform = QTransform()
            transform.rotate(15)
            rotated_pixmap = pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
            scaled_pixmap = rotated_pixmap.scaled(
                600, 600, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText("[ Graphic Placeholder ]")
            
        graphic_layout.addWidget(self.image_label)
        body_layout.addWidget(graphic_container, stretch=4)
        
        root_layout.addLayout(body_layout)
        
        # Set Default initial language loading string state
        self.update_language("English")

    def update_language(self, language_name: str):
        """Finds translation mappings and sets component UI values synchronously."""
        lang_data = TRANSLATIONS.get(language_name)
        if not lang_data:
            return
            
        # Dynamically change the text values across instances
        self.nav_home.setText(lang_data["home"])
        self.nav_templates.setText(lang_data["templates"])
        self.nav_quizzes.setText(lang_data["quizzes"])
        self.hero_title.setText(lang_data["title"])
        self.hero_desc.setText(lang_data["desc"])
        self.play_btn.setText(lang_data["play"])
        self.create_btn.setText(lang_data["create"])
        self.sign_out_btn.setText(lang_data["sign_out"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = QuizLandingUI()
    ui.show()
    sys.exit(app.exec())

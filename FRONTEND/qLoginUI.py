import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
for parent_check in [script_dir, script_dir.parent, script_dir / "ui", script_dir / "styles"]:
    if (parent_check / "styles.py").exists() and str(parent_check) not in sys.path:
        sys.path.append(str(parent_check))
        break

from PyQt6.QtCore import Qt, pyqtSignal, QRegularExpression
from PyQt6.QtGui import QColor, QRegularExpressionValidator, QPixmap, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QFrame,
    QStackedWidget,
    QGraphicsDropShadowEffect,
    QMessageBox,
    QSizePolicy
)

backend_dir = Path(__file__).resolve().parent / ".." / "BACKEND"
sys.path.insert(0, str(backend_dir))

from users import verify_user, create_user,initialize_storage
import styles as st

WINDOW_SIZE = (1280, 720)


def _password_field() -> QLineEdit:
    edit = QLineEdit()
    edit.setEchoMode(QLineEdit.EchoMode.Password)
    edit.setStyleSheet(st.INPUT_FIELD)
    
    no_space_regex = QRegularExpression(r"^\S*$")
    validator = QRegularExpressionValidator(no_space_regex, edit)
    edit.setValidator(validator)
    
    return edit


def _page_style() -> str:
    return f"""
    QWidget#page {{
        background-color: {st.Colors.BG_MAIN};
    }}
    QLabel {{
        font-family: 'Segoe UI', Arial, sans-serif;
        background: transparent;
    }}
    QLabel#header {{
        background-color: {st.Colors.PRIMARY};
        color: {st.Colors.TEXT_LIGHT};
        font-size: 22px;
        font-weight: bold;
        padding: 10px 20px;
    }}
    QLabel#pageTitle {{
        color: {st.Colors.TEXT_DARK};
        font-size: 38px;
        font-weight: bold;
    }}
    QLabel#hint {{
        color: {st.Colors.TEXT_MUTED};
        font-size: 14px;
    }}
    QFrame#card {{
        background-color: {st.Colors.PRIMARY};
        border: 4px solid {st.Colors.GOLD};
        border-radius: 24px;
    }}
    QFrame#card QLabel {{
        color: {st.Colors.TEXT_LIGHT};
        font-size: 18px;
        border: none;
    }}
    QLabel#cardTitle {{
        color: {st.Colors.TEXT_LIGHT};
        font-size: 22px;
    }}
    QPushButton#link {{
        background: transparent;
        border: none;
        color: {st.Colors.PRIMARY};
        text-decoration: underline;
        font-size: 13px;
    }}
    QPushButton#link:hover {{
        color: {st.Colors.PRIMARY_HOVER};
    }}
    """


class LoginUI(QWidget):
    logged_in = pyqtSignal(str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self.pages = QStackedWidget()
        outer.addWidget(self.pages)

        self.pages.addWidget(self._create_register_page())  
        self.pages.addWidget(self._create_login_page())   

    def _build_page(self, title, hint, rows, btn_text, on_btn, link_text, on_link) -> QWidget:
        page = QWidget()
        page.setObjectName("page")
        page.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        page.setStyleSheet(_page_style())

        v = QVBoxLayout(page)
        v.setContentsMargins(0, 0, 0, 20)
        v.setSpacing(8)

        header = QLabel("MindSpark")
        header.setObjectName("header")
        v.addWidget(header)
        v.addSpacing(10)

        t = QLabel(title)
        t.setObjectName("pageTitle")
        t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(t)

        hint_row = QHBoxLayout()
        hint_row.addStretch()
        h = QLabel(hint)
        h.setObjectName("hint")
        h.setFixedWidth(380)
        hint_row.addWidget(h)
        hint_row.addStretch()
        v.addLayout(hint_row)

        card = QFrame()
        card.setObjectName("card")
        card.setMinimumWidth(300)
        card.setMaximumWidth(480)
        card.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
        glow = QGraphicsDropShadowEffect(card)
        glow.setBlurRadius(20)
        glow.setOffset(0, 4)
        glow.setColor(QColor(255, 200, 0, 160))
        card.setGraphicsEffect(glow)

        grid = QGridLayout(card)
        grid.setContentsMargins(20, 16, 20, 16)
        grid.setVerticalSpacing(14)
        
        logo_container = QWidget()
        logo_container.setStyleSheet("background: transparent;")
        box = QVBoxLayout(logo_container)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(4)
        box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        card_title = QLabel()
        grid.addWidget(card_title, 0, 0, 1, 2)
        
        logo_path = script_dir / "logo.png"
        pixmap = QPixmap(str(logo_path))
        scaled_pixmap = pixmap.scaled(300, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        card_title.setPixmap(scaled_pixmap)
        card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        name_lbl = QLabel("MindSpark")
        name_lbl.setObjectName("cardTitle")
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        box.addWidget(card_title)
        box.addWidget(name_lbl)

        grid.addWidget(logo_container, 0, 0, 1, 2)
        
        for i, (label, widget) in enumerate(rows, start=2):
            lbl = QLabel(label)
            lbl.setObjectName("field")
            grid.addWidget(lbl, i, 0)
            grid.addWidget(widget, i, 1)
            
        grid.setRowStretch(len(rows) + 2, 1)
        grid.setColumnStretch(1, 1)

        card_row = QHBoxLayout()
        card_row.addStretch()
        card_row.addWidget(card)
        card_row.addStretch()
        v.addLayout(card_row)
        v.addSpacing(10)

        btn = QPushButton(btn_text)
        btn.setStyleSheet(st.BTN_PRIMARY)
        btn.setFixedWidth(240)
        if on_btn:
            btn.clicked.connect(on_btn)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn)
        btn_row.addStretch()
        v.addLayout(btn_row)

        link = QPushButton(link_text)
        link.setObjectName("link")
        link.setFlat(True)
        link.clicked.connect(on_link)
        v.addWidget(link, alignment=Qt.AlignmentFlag.AlignCenter)

        v.addStretch()
        return page

    def do_register(self):
        username = self.reg_user.text().strip()
        password = self.reg_pass.text()
        role = self.reg_role.currentText()

        if not username or not password:
            QMessageBox.critical(self, "Missing Information", "Username and password are required.")
        elif len(password) < 6:
            QMessageBox.critical(self, "Weak Password", "Password must be at least 6 characters.")
        elif not create_user(username, password, role):
            QMessageBox.critical(self, "Username Taken", "That username already exists.")
        else:
            QMessageBox.information(self, "Account Created", "Account created! You can now log in.")
            self.reg_user.clear()
            self.reg_pass.clear()
            self.login_user.setText(username)        
            self.pages.setCurrentIndex(1)
            
    def _create_register_page(self) -> QWidget:
        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("Username")
        self.reg_user.setStyleSheet(st.INPUT_FIELD)
        self.reg_pass = _password_field()
        self.reg_pass.setPlaceholderText("(min. 6 characters)") 
        self.reg_pass.returnPressed.connect(self.do_register)
        self.reg_role = QComboBox()
        self.reg_role.setStyleSheet(st.COMBOBOX)
        self.reg_role.addItems(["Student", "Teacher"])

        return self._build_page(
            "Register",
            "Please Register to login",
            [("Username", self.reg_user), ("Password", self.reg_pass), ("Role", self.reg_role)],
            "Sign-up", self.do_register,
            "Already have an account? Log in",
            lambda: self.pages.setCurrentIndex(1),   
        )

    def do_login(self):
        username = self.login_user.text().strip()
        password = self.login_pass.text()

        if not username or not password:
            QMessageBox.critical(self, "Missing Information", "Enter your username and password.")
            return

        role = verify_user(username, password)      
        if role is None:
            QMessageBox.critical(self, "Login Failed", "Incorrect username or password.")
            self.login_pass.clear()
            return

        self.reset()
        self.logged_in.emit(username, role)  

    def _create_login_page(self) -> QWidget:
        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("Username")
        self.login_user.setStyleSheet(st.INPUT_FIELD)
        self.login_pass = _password_field()
        self.login_pass.setPlaceholderText("Password")
        self.login_pass.returnPressed.connect(self.do_login)

        return self._build_page(
            "Login",
            "Please Log in to continue",
            [("Username", self.login_user), ("Password", self.login_pass)],
            "Log-in",
            self.do_login,                                      
            "Create an account",
            lambda: self.pages.setCurrentIndex(0),   
        )

    def reset(self):
        for w in (self.reg_user, self.reg_pass, self.login_user, self.login_pass):
            w.clear()
        self.reg_role.setCurrentIndex(0)
        self.pages.setCurrentIndex(0)


if __name__ == "__main__":

    initialize_storage()   
    app = QApplication(sys.argv)

    window = LoginUI()
    window.resize(*WINDOW_SIZE)
    window.setWindowTitle("MindSpark")
    window.setWindowIcon(QIcon(str("logo.png")))
    window.logged_in.connect(lambda u, r: print("Logged in:", u, r))
    window.show()

    sys.exit(app.exec())

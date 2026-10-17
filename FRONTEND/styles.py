# styles.py

class Colors:
    PRIMARY = "#6b1d24"
    PRIMARY_HOVER = "#52151b"
    PRIMARY_LIGHT = "#fcf2f3"
    PRIMARY_BORDER = "#f2c2c5"
    PRIMARY_DISABLED = "#d19ba0"

    ACCENT = "#ca8a04"
    ACCENT_BG = "#fef9c3"
    ACCENT_BORDER = "#facc15"
    GOLD = "#FFD700"

    BG_MAIN = "#f4f6f8"
    CARD_BG = "#ffffff"
    HOVER_BG = "#f8fafc"

    TEXT_DARK = "#0f172a"
    TEXT_MUTED = "#64748b"
    TEXT_MEDIUM = "#334155"
    TEXT_LIGHT = "#ffffff"

    BORDER_LIGHT = "#e2e8f0"
    BORDER_DIVIDER = "#f1f5f9"
    BORDER_INPUT = "#cbd5e1"

MAIN_WINDOW = f"background-color: {Colors.BG_MAIN};"

CARD_FRAME = f"""
    QFrame {{
        background-color: {Colors.CARD_BG};
        border: 1px solid {Colors.BORDER_LIGHT};
        border-radius: 12px;
    }}
"""

CARD_FRAME_ACCENT = f"""
    QFrame {{
        background-color: {Colors.PRIMARY};
        border: 3px solid {Colors.GOLD};
        border-radius: 20px;
    }}
"""

DIVIDER = f"""
    background-color: {Colors.BORDER_DIVIDER};
    border: none;
    min-height: 1px;
    max-height: 1px;
"""

LABEL_TITLE = f"""
    color: {Colors.TEXT_DARK};
    font-size: 20px;
    font-weight: bold;
    border: none;
    margin-top: 10px;
"""

LABEL_SUBHEADER = f"""
    color: {Colors.TEXT_MEDIUM};
    font-size: 13px;
    font-weight: bold;
    border: none;
"""

LABEL_MUTED = f"""
    color: {Colors.TEXT_MUTED};
    font-size: 13px;
    border: none;
"""

LABEL_SIDEBAR_HEADER = f"""
    font-size: 15px;
    font-weight: bold;
    color: {Colors.TEXT_DARK};
    border: none;
"""

LABEL_COUNTER_ACTIVE = f"""
    font-size: 12px;
    font-weight: bold;
    color: {Colors.ACCENT};
    border: none;
"""

SIDEBAR_SCROLL_AREA = f"""
    QScrollArea {{
        border: none;
        background-color: transparent;
    }}
    QScrollArea QScrollBar:vertical {{
        width: 8px;
        background: transparent;
        margin: 0 2px;
    }}
    QScrollArea QScrollBar::handle:vertical {{
        background: #b5b5b5;
        border-radius: 4px;
        min-height: 24px;
    }}
    QScrollArea QScrollBar::add-line:vertical,
    QScrollArea QScrollBar::sub-line:vertical {{
        height: 0;
    }}
"""

BTN_PRIMARY = f"""
    QPushButton {{
        background-color: {Colors.PRIMARY};
        color: {Colors.TEXT_LIGHT};
        border: none;
        border-radius: 6px;
        padding: 8px 20px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {Colors.PRIMARY_HOVER};
    }}
    QPushButton:disabled {{
        background-color: {Colors.PRIMARY_DISABLED};
    }}
"""

BTN_SECONDARY = f"""
    QPushButton {{
        background-color: {Colors.CARD_BG};
        color: {Colors.TEXT_MEDIUM};
        border: 1px solid {Colors.BORDER_INPUT};
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
    }}
    QPushButton:hover {{
        background-color: {Colors.BORDER_DIVIDER};
    }}
    QPushButton:disabled {{
        background-color: {Colors.BORDER_LIGHT};
        color: #94a3b8;
    }}
"""

BTN_PILL = f"""
    QPushButton {{
        background-color: {Colors.PRIMARY};
        color: {Colors.TEXT_LIGHT};
        border: none;
        border-radius: 15px;
        padding: 9px 20px;
        font-size: 14px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {Colors.PRIMARY_HOVER};
    }}
    QPushButton:disabled {{
        background-color: {Colors.PRIMARY_DISABLED};
    }}
"""

BTN_ROUND_DELETE = f"""
    QPushButton {{
        background-color: #ff2a2a;
        color: {Colors.TEXT_LIGHT};
        border: none;
        border-radius: 17px;
        min-width: 34px;
        max-width: 34px;
        min-height: 34px;
        max-height: 34px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: #cc0000;
    }}
"""

# --- Header / Ribbon Styles ---

HEADER_CONTAINER = f"""
    QFrame {{
        background-color: {Colors.PRIMARY};
        border: none;
    }}
"""

RIBBON_CONTAINER = f"""
    QFrame {{
        background-color: {Colors.PRIMARY};
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 0px;
        border: none;
    }}
"""

LABEL_RIBBON_TITLE = f"""
    color: {Colors.TEXT_LIGHT};
    font-size: 18px;
    font-weight: bold;
    border: none;
"""

LABEL_RIBBON_SUBTITLE = f"""
    color: {Colors.PRIMARY_BORDER};
    font-size: 13px;
    border: none;
"""

# --- Inputs & Common Controls ---

INPUT_FIELD = f"""
    QLineEdit {{
        background: {Colors.CARD_BG};
        border: 1px solid {Colors.BORDER_INPUT};
        border-radius: 12px;
        padding: 6px 14px;
        font-size: 14px;
        color: {Colors.TEXT_DARK};
    }}
    QLineEdit:focus {{
        border: 2px solid {Colors.PRIMARY};
    }}
"""

COMBOBOX = f"""
    QComboBox {{
        background: {Colors.CARD_BG};
        border: 1px solid {Colors.BORDER_INPUT};
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 14px;
        color: {Colors.TEXT_DARK};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox QAbstractItemView {{
        background: {Colors.CARD_BG};
        color: {Colors.TEXT_DARK};
        selection-background-color: {Colors.PRIMARY};
        selection-color: {Colors.TEXT_LIGHT};
        font-size: 14px;
    }}
"""

SPINBOX = f"""
    QSpinBox {{
        background: {Colors.CARD_BG};
        border: 1px solid {Colors.BORDER_INPUT};
        border-radius: 8px;
        padding: 4px 8px;
        font-size: 14px;
        color: {Colors.TEXT_DARK};
    }}
"""

# --- Dynamic Helper Functions ---

def option_frame(is_selected: bool) -> str:
    if is_selected:
        return f"""
            QFrame {{
                background-color: {Colors.PRIMARY_LIGHT};
                border: 2px solid {Colors.PRIMARY};
                border-radius: 8px;
            }}
            QRadioButton {{
                color: {Colors.PRIMARY_HOVER};
                font-size: 14px;
                font-weight: bold;
                border: none;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid {Colors.PRIMARY};
                background: {Colors.CARD_BG};
            }}
            QRadioButton::indicator:checked {{
                background-color: {Colors.PRIMARY};
                border: 2px solid {Colors.PRIMARY};
                border-radius: 10px;
            }}
        """
    return f"""
        QFrame {{
            background-color: {Colors.CARD_BG};
            border: 1px solid {Colors.BORDER_LIGHT};
            border-radius: 8px;
        }}
        QFrame:hover {{
            border-color: {Colors.BORDER_INPUT};
            background-color: {Colors.HOVER_BG};
        }}
        QRadioButton {{
            color: {Colors.TEXT_MEDIUM};
            font-size: 14px;
            border: none;
        }}
        QRadioButton::indicator {{
            width: 20px;
            height: 20px;
            border-radius: 10px;
            border: 2px solid {Colors.PRIMARY};
            background: {Colors.CARD_BG};
        }}
        QRadioButton::indicator:checked {{
            background-color: {Colors.PRIMARY};
            border: 2px solid {Colors.PRIMARY};
            border-radius: 10px;
        }}
    """

def nav_button(state: str) -> str:
    base_padding = "text-align: left; padding: 8px 12px; border-radius: 6px; font-size: 13px;"
    
    if state == "current":
        return f"""
            QPushButton {{
                {base_padding}
                background-color: {Colors.PRIMARY_LIGHT};
                color: {Colors.PRIMARY};
                border: 1px solid {Colors.PRIMARY_BORDER};
                font-weight: bold;
            }}
        """
    elif state == "answered":
        return f"""
            QPushButton {{
                {base_padding}
                background-color: {Colors.ACCENT_BG};
                color: {Colors.ACCENT};
                border: 1px solid {Colors.ACCENT_BORDER};
                font-weight: 500;
            }}
        """
    else:
        return f"""
            QPushButton {{
                {base_padding}
                background-color: {Colors.CARD_BG};
                color: {Colors.TEXT_MUTED};
                border: 1px solid {Colors.BORDER_DIVIDER};
            }}
            QPushButton:hover {{
                background-color: {Colors.HOVER_BG};
                border-color: {Colors.BORDER_INPUT};
            }}
        """
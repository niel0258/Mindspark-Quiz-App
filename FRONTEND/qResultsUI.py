import sys
import os
import json
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
script_dir = Path(__file__).resolve().parent
backend_dir = script_dir / ".." / "BACKEND"
sys.path.insert(0, str(backend_dir))

import styles as st
from database import get_quiz_details, RESULTS_DIR


class QuizResultWindow(QMainWindow):
    def __init__(self, username="student", quiz_id=1):
        super().__init__()
        self.setWindowTitle("Quiz Results")
        self.setWindowIcon(QIcon(str(script_dir / "logo.png")))
        self.resize(1280, 720)
        if hasattr(st, "MAIN_WINDOW"):
          self.setStyleSheet(st.MAIN_WINDOW)
        else:
          self.setStyleSheet("background-color: #f4f4f4;")

        # Fetch quiz header details
        details = get_quiz_details(quiz_id)
        if details and details[0]:
            q_info = details[0]
            quiz_name = q_info[0] if len(q_info) > 0 else "Quiz name"
            subject_name = q_info[1] if len(q_info) > 1 else "Subject name"
        else:
            quiz_name = "Quiz name"
            subject_name = "Subject name"

        # Fetch score details
        result_data = self._fetch_latest_result(username, quiz_id)
        score = result_data.get("score", 0)
        total_points = result_data.get("total_points", 0)
        correct_count = result_data.get("correct_count", score)
        incorrect_count = result_data.get("incorrect_count", max(0, total_points - score))
        
        raw_answers = result_data.get("answers", [])
        if isinstance(raw_answers, dict):
            answers = list(raw_answers.values())
        elif isinstance(raw_answers, list):
            answers = raw_answers
        else:
            answers = []

        # Main Layout Setup
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header Section
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #581414; border: none;")
        header_frame.setFixedHeight(80)

        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 10, 30, 10)
        header_layout.setSpacing(2)

        q_title_lbl = QLabel(quiz_name)
        q_title_lbl.setStyleSheet("color: white; font-size: 24px; font-weight: bold; border: none;")

        sub_title_lbl = QLabel(subject_name)
        sub_title_lbl.setStyleSheet("color: #e0e0e0; font-size: 14px; border: none;")

        header_layout.addWidget(q_title_lbl)
        header_layout.addWidget(sub_title_lbl)

        # Center Container hosting both Left (Progress) and Right (Review) cards
        center_container = QWidget()
        center_layout = QHBoxLayout(center_container)
        center_layout.setContentsMargins(40, 30, 40, 30)
        center_layout.setSpacing(30)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ==========================================
        # LEFT CARD: Your Progress
        # ==========================================
        progress_card = QFrame()
        progress_card.setFixedSize(400, 500)
        progress_card.setStyleSheet("""
            QFrame {
                background-color: #581414;
                border: 3px solid #f39c12;
                border-radius: 20px;
            }
        """)

        progress_layout = QVBoxLayout(progress_card)
        progress_layout.setContentsMargins(25, 25, 25, 25)
        progress_layout.setSpacing(15)

        progress_title = QLabel("Your Progress")
        progress_title.setStyleSheet("color: white; font-size: 22px; font-weight: bold; border: none;")
        progress_layout.addWidget(progress_title)

        # Score Banner
        score_banner = QFrame()
        score_banner.setStyleSheet("background-color: #dcdcdc; border-radius: 15px; border: none;")
        score_banner.setFixedHeight(80)
        score_banner_layout = QHBoxLayout(score_banner)
        score_banner_layout.setContentsMargins(20, 10, 20, 10)

        score_lbl = QLabel(f"{score} / {total_points}")
        score_lbl.setStyleSheet("color: black; font-size: 18px; font-weight: bold; border: none;")
        
        # Load and display Chart.png
        chart_icon = QLabel()
        chart_pixmap = QPixmap(str(script_dir / "Chart.png"))
        if not chart_pixmap.isNull():
            # Scale image smoothly to fit inside the banner height
            chart_icon.setPixmap(chart_pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            # Fallback text if the image path is not found
            chart_icon.setText("📊")
            chart_icon.setStyleSheet("font-size: 36px; border: none;")
            
        chart_icon.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        score_banner_layout.addWidget(score_lbl)
        score_banner_layout.addStretch()
        score_banner_layout.addWidget(chart_icon)
        progress_layout.addWidget(score_banner)

        # Correct Pill
        correct_pill = QFrame()
        correct_pill.setStyleSheet("background-color: #dcdcdc; border-radius: 15px; border: none;")
        correct_pill.setFixedHeight(50)
        correct_layout = QHBoxLayout(correct_pill)
        correct_layout.setContentsMargins(15, 5, 15, 5)

        correct_left = QLabel("✔ Correct")
        correct_left.setStyleSheet("color: #27ae60; font-size: 15px; font-weight: bold; border: none;")
        correct_right = QLabel(f"Total of correct #{correct_count}")
        correct_right.setStyleSheet("color: black; font-size: 13px; border: none;")

        correct_layout.addWidget(correct_left)
        correct_layout.addStretch()
        correct_layout.addWidget(correct_right)
        progress_layout.addWidget(correct_pill)

        # Incorrect Pill
        incorrect_pill = QFrame()
        incorrect_pill.setStyleSheet("background-color: #dcdcdc; border-radius: 15px; border: none;")
        incorrect_pill.setFixedHeight(50)
        incorrect_layout = QHBoxLayout(incorrect_pill)
        incorrect_layout.setContentsMargins(15, 5, 15, 5)

        incorrect_left = QLabel("✖ Incorrect")
        incorrect_left.setStyleSheet("color: #c0392b; font-size: 15px; font-weight: bold; border: none;")
        incorrect_right = QLabel(f"Total of incorrect #{incorrect_count}")
        incorrect_right.setStyleSheet("color: black; font-size: 13px; border: none;")

        incorrect_layout.addWidget(incorrect_left)
        incorrect_layout.addStretch()
        incorrect_layout.addWidget(incorrect_right)
        progress_layout.addWidget(incorrect_pill)

        progress_layout.addStretch()

        # Return Button
        return_btn = QPushButton("Return")
        return_btn.setFixedSize(180, 40)
        return_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        return_btn.clicked.connect(self.close)
        progress_layout.addWidget(return_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # ==========================================
        # RIGHT CARD: Review your Answers
        # ==========================================
        review_card = QFrame()
        review_card.setFixedSize(400, 500)
        review_card.setStyleSheet("""
            QFrame {
                background-color: #581414;
                border: 3px solid #f39c12;
                border-radius: 20px;
            }
        """)

        review_layout = QVBoxLayout(review_card)
        review_layout.setContentsMargins(20, 20, 20, 20)

        review_title = QLabel("Review your Answers")
        review_title.setStyleSheet("color: white; font-size: 22px; font-weight: bold; border: none;")
        review_layout.addWidget(review_title)

        # Scrollable Question Container
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #3a0d0d;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #f39c12;
                border-radius: 5px;
            }
        """)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 5, 0, 5)
        scroll_layout.setSpacing(15)

        # Populate Question Cards
        items_to_render = answers if answers else []

        for item in items_to_render:
            q_box = QFrame()
            q_box.setStyleSheet("background-color: #dcdcdc; border-radius: 15px; border: none;")
            q_box_layout = QVBoxLayout(q_box)
            q_box_layout.setContentsMargins(15, 10, 15, 15)

            # Subheader inside question card
            header_sub = QHBoxLayout()
            q_type = QLabel(item.get("type", "Question"))
            q_type.setStyleSheet("color: white; font-weight: bold; font-size: 11px; background-color: #581414; padding: 2px 6px; border-radius: 4px;")
            
            is_correct = item.get("is_correct", False)
            status_lbl = QLabel("✔ Correct" if is_correct else "✖ Incorrect")
            status_lbl.setStyleSheet(f"color: {'#27ae60' if is_correct else '#c0392b'}; font-weight: bold; font-size: 12px;")

            header_sub.addWidget(q_type)
            header_sub.addStretch()
            header_sub.addWidget(status_lbl)
            q_box_layout.addLayout(header_sub)

            # Question Text
            q_text = QLabel(item.get("question", "Question prompt"))
            q_text.setStyleSheet("color: black; font-size: 16px; font-weight: bold; margin-top: 5px; margin-bottom: 5px; border: none;")
            q_box_layout.addWidget(q_text)

            selected = str(item.get("selected_option", "None"))
            correct = str(item.get("correct_option", "None"))

            # Display Selected Answer Pill
            sel_pill = QLabel(f"  Your Answer:  {selected}")
            sel_pill.setStyleSheet(f"""
                QLabel {{
                    background-color: {'#d4edda' if is_correct else '#f8d7da'};
                    color: {'#155724' if is_correct else '#721c24'};
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 6px;
                    margin-top: 2px;
                }}
            """)
            q_box_layout.addWidget(sel_pill)

            # Display Correct Answer Pill if the student was wrong
            if not is_correct:
                corr_pill = QLabel(f"  Correct Answer:  {correct}")
                corr_pill.setStyleSheet("""
                    QLabel {
                        background-color: #d4edda;
                        color: #155724;
                        font-size: 13px;
                        font-weight: bold;
                        border-radius: 10px;
                        padding: 6px;
                        margin-top: 2px;
                    }
                """)
                q_box_layout.addWidget(corr_pill)

            scroll_layout.addWidget(q_box)

        scroll.setWidget(scroll_content)
        review_layout.addWidget(scroll)

        # Add components to main layout
        center_layout.addWidget(progress_card)
        center_layout.addWidget(review_card)

        main_layout.addWidget(header_frame)
        main_layout.addWidget(center_container)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _fetch_latest_result(self, username, quiz_id):
        """Finds and parses the newest student result JSON file by modification time."""
        try:
            if not os.path.exists(RESULTS_DIR):
                return {}

            clean_username = username.strip().lower()
            files = os.listdir(RESULTS_DIR)

            matching_files = [
                os.path.join(RESULTS_DIR, f) for f in files
                if clean_username in f.lower() and str(quiz_id) in f
            ]

            if not matching_files:
                return {}

            # Sort strictly by file modification time (newest first)
            matching_files.sort(key=lambda filepath: os.path.getmtime(filepath), reverse=True)
            latest_filepath = matching_files[0]

            with open(latest_filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                raw_answers = data.get("answers", [])
                if isinstance(raw_answers, dict):
                    data["answers"] = list(raw_answers.values())
                
                return data
        except Exception as e:
            print(f"Error reading result file in results UI: {e}")
            return {}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizResultWindow(username="student", quiz_id=1)
    window.show()
    sys.exit(app.exec())


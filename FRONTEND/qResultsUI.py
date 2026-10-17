import sys
import os
import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pathlib import Path
backend_dir = Path(__file__).resolve().parent / ".." / "BACKEND"
sys.path.insert(0, str(backend_dir))

import styles as st
from database import get_quiz_details, RESULTS_DIR

class QuizResultWindow(QMainWindow):
    def __init__(self, username="student", quiz_id=1):
        super().__init__()
        self.setWindowTitle("Quiz Results")
        self.resize(1280, 720)
        self.setStyleSheet(st.MAIN_WINDOW)

        # Robust data unpacking for quiz details
        details = get_quiz_details(quiz_id)
        if details and details[0]:
            q_info = details[0]
            quiz_name = q_info[0] if len(q_info) > 0 else "Quiz name"
            subject_name = q_info[1] if len(q_info) > 1 else "Subject name"
        else:
            quiz_name = "Quiz name"
            subject_name = "Subject name"

        # Direct, robust retrieval matching any student result file saved by qTakeUI
        score, total_points, percentage = self._fetch_latest_score(username, quiz_id)
        score_text = f"{int(percentage)}%"
        badge_text = f"{score}/{total_points}"

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header_frame = QFrame()
        header_frame.setStyleSheet(st.HEADER_CONTAINER)
        header_frame.setFixedHeight(70)

        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 8, 30, 8)
        header_layout.setSpacing(2)

        q_title_lbl = QLabel(quiz_name)
        q_title_lbl.setStyleSheet(st.LABEL_RIBBON_TITLE)

        sub_title_lbl = QLabel(subject_name)
        sub_title_lbl.setStyleSheet(st.LABEL_RIBBON_SUBTITLE)

        header_layout.addWidget(q_title_lbl)
        header_layout.addWidget(sub_title_lbl)

        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 20, 0, 20)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setFixedSize(360, 360)
        card.setStyleSheet(st.CARD_FRAME_ACCENT)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 30, 20, 20)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        stats_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        circle_score = QLabel(score_text)
        circle_score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        circle_score.setFixedSize(160, 160)
        circle_score.setStyleSheet(
            """
            QLabel {
                background-color: #D9D9D9;
                color: #000000;
                font-weight: bold;
                font-size: 35px;
                border-radius: 80px;
                border: none;
            }
            """
        )

        score_badge = QLabel(badge_text)
        score_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_badge.setFixedSize(140, 38)
        score_badge.setStyleSheet(
            """
            QLabel {
                background-color: #D9D9D9;
                color: #000000;
                font-weight: bold;
                font-size: 15px;
                border-radius: 19px;
                border: none;
            }
            """
        )

        stats_layout.addWidget(circle_score)
        stats_layout.addWidget(score_badge)

        return_btn = QPushButton("Return")
        return_btn.setFixedSize(160, 36)
        return_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return_btn.setStyleSheet(st.BTN_PRIMARY)
        return_btn.clicked.connect(self.close)

        card_layout.addLayout(stats_layout)
        card_layout.addStretch()
        card_layout.addWidget(
            return_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )

        center_layout.addWidget(card)

        main_layout.addWidget(header_frame)
        main_layout.addWidget(center_container)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _fetch_latest_score(self, username, quiz_id):
        """Directly scans and parses student result JSON files exported by qTakeUI."""
        try:
            if not os.path.exists(RESULTS_DIR):
                return 0, 0, 0.0

            clean_username = username.strip().lower()
            files = os.listdir(RESULTS_DIR)
            
            # Match any file containing the username and quiz ID combination
            matching_files = [
                f for f in files 
                if clean_username in f.lower() and f"_quiz_{quiz_id}_" in f.lower()
            ]

            if not matching_files:
                return 0, 0, 0.0

            # Sort descending by filename (since timestamp attempt_id is part of the filename)
            matching_files.sort(reverse=True)
            latest_filepath = os.path.join(RESULTS_DIR, matching_files[0])

            with open(latest_filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                score = data.get("score", 0)
                total_points = data.get("total_points", 0)
                percentage = data.get("percentage", 0.0)
                return score, total_points, percentage
        except Exception as e:
            print(f"Error reading result file directly in results UI: {e}")
            return 0, 0, 0.0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizResultWindow(username="student", quiz_id=1)
    window.show()
    sys.exit(app.exec())
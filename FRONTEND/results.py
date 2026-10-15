import sys
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


class QuizResultWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Results")
        self.resize(1920, 1080)
        self.setStyleSheet("background-color: #FFFFFF;")

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ------------------ TOP HEADER ------------------
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #5C1313;")
        header_frame.setFixedHeight(70)

        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 8, 30, 8)
        header_layout.setSpacing(2)

        quiz_title = QLabel("Quiz name")
        quiz_title.setStyleSheet(
            "color: white; font-size: 22px; font-weight: bold; font-family: sans-serif;"
        )

        subject_title = QLabel("Subject name")
        subject_title.setStyleSheet(
            "color: white; font-size: 14px; font-family: sans-serif;"
        )

        header_layout.addWidget(quiz_title)
        header_layout.addWidget(subject_title)

        # ------------------ CENTER CONTENT ------------------
        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.setContentsMargins(0, 20, 0, 20)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setFixedSize(360, 360)
        card.setStyleSheet(
            """
            QFrame {
                background-color: #5C1313;
                border: 3px solid #FFD700;
                border-radius: 20px;
            }
            """
        )

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 30, 20, 20)


        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        stats_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    
        circle_score = QLabel("50%")
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

        # Score / Total Pill Badge
        score_badge = QLabel("50/100")
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

        # Return Button
        return_btn = QPushButton("Return")
        return_btn.setFixedSize(160, 36)
        return_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #000000;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
                border-radius: 18px;
                border: none;
            }
            QPushButton:hover {
                background-color: #222222;
            }
            """
        )

        card_layout.addLayout(stats_layout)
        card_layout.addStretch()
        card_layout.addWidget(
            return_btn, alignment=Qt.AlignmentFlag.AlignCenter
        )

        center_layout.addWidget(card)

        # Add Header and Center Widget to Main Layout
        main_layout.addWidget(header_frame)
        main_layout.addWidget(center_container)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizResultWindow()
    window.show()
    sys.exit(app.exec())
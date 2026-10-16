import os
import sqlite3
import json

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "student_results_storage")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    initialize_quiz_storage()
    return conn

def initialize_quiz_storage():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS quizzes (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       quiz_name TEXT NOT NULL,
                       subject_name TEXT NOT NULL,
                       creator TEXT NOT NULL
                   )"""
            )
            conn.execute(
                """CREATE TABLE IF NOT EXISTS questions (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       quiz_id INTEGER NOT NULL,
                       q_type TEXT NOT NULL,
                       question TEXT NOT NULL,
                       points INTEGER NOT NULL,
                       choices TEXT NOT NULL,
                       correct_answer INTEGER,
                       FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
                   )"""
            )
    finally:
        conn.close()

def save_quiz_to_db(quiz_name, subject_name, creator, questions_data):
    conn = get_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO quizzes (quiz_name, subject_name, creator) VALUES (?, ?, ?)",
                (quiz_name, subject_name, creator)
            )
            quiz_id = cursor.lastrowid
            
            for q in questions_data:
                choices_str = json.dumps(q.get("choices", []))
                cursor.execute(
                    """INSERT INTO questions (quiz_id, q_type, question, points, choices, correct_answer)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (quiz_id, q["qType"], q["question"], q["points"], choices_str, q["right_answer"])
                )
        return True
    except Exception as e:
        print(f"Error saving quiz: {e}")
        return False
    finally:
        conn.close()

def get_all_quizzes():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, quiz_name, subject_name, creator FROM quizzes")
        return cursor.fetchall()
    finally:
        conn.close()

def get_quiz_details(quiz_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        q_info = cursor.execute("SELECT quiz_name, subject_name FROM quizzes WHERE id = ?", (quiz_id,)).fetchone()
        if not q_info:
            return None, []
        
        rows = cursor.execute(
            "SELECT q_type, question, points, choices, correct_answer FROM questions WHERE quiz_id = ?",
            (quiz_id,)
        ).fetchall()
        
        questions = []
        for r in rows:
            questions.append({
                "type": r[0],
                "question": r[1],
                "points": r[2],
                "choices": json.loads(r[3]),
                "correct": r[4]
            })
        return q_info, questions
    finally:
        conn.close()

def save_student_result(username, quiz_id, score, total_points, percentage, answers_dict):
    try:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        import time
        attempt_id = int(time.time() * 1000)
        filename = f"{username}_quiz_{quiz_id}_{attempt_id}.json"
        filepath = os.path.join(RESULTS_DIR, filename)

        result_data = {
            "attempt_id": attempt_id,
            "username": username,
            "quiz_id": quiz_id,
            "score": score,
            "total_points": total_points,
            "percentage": percentage,
            "answers": answers_dict
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving result file: {e}")
        return False

def get_student_latest_result(username, quiz_id):
    try:
        if not os.path.exists(RESULTS_DIR):
            return None
        
        clean_username = username.strip().lower()
        files = os.listdir(RESULTS_DIR)
        
        user_quiz_files = [
            f for f in files 
            if f.lower().startswith(f"{clean_username}_quiz_{quiz_id}_".lower())
        ]
        
        if not user_quiz_files:
            print(f"No result files found for username: '{username}' and quiz_id: {quiz_id}")
            return None
        
        user_quiz_files.sort(reverse=True)
        latest_file = os.path.join(RESULTS_DIR, user_quiz_files[0])

        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return (
                data.get("score", 0),
                data.get("total_points", 0),
                data.get("percentage", 0.0),
                json.dumps(data.get("answers", {}))
            )
    except Exception as e:
        print(f"Error reading result file: {e}")
        return None


def delete_quiz_from_db(quiz_id):
    conn = get_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
        return True
    except Exception as e:
        print(f"Error deleting quiz: {e}")
        return False
    finally:
        conn.close()
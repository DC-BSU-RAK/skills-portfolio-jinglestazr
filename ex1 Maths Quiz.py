import tkinter as tk
from tkinter import messagebox
import random

# -----------------------------
# Color Scheme
# -----------------------------
BG_COLOR = "#f0f8ff"  # Alice Blue
HEADER_COLOR = "#4a90e2"  # Bright Blue
BUTTON_COLOR = "#5cb85c"  # Success Green
BUTTON_HOVER = "#4cae4c"  # Darker Green
DANGER_COLOR = "#d9534f"  # Red
TEXT_COLOR = "#2c3e50"  # Dark Blue-Gray
LIGHT_TEXT = "#ffffff"  # White

# -----------------------------
# Helper Functions
# -----------------------------

def displayMenu():
    """Display difficulty selection menu."""
    clear_window()
    
    # Header
    header = tk.Label(root, text="🧮 ARITHMETIC QUIZ GAME 🧮", 
                     font=("Comic Sans MS", 22, "bold"), 
                     bg=HEADER_COLOR, fg=LIGHT_TEXT, pady=15)
    header.pack(fill=tk.X)
    
    tk.Label(root, text="Choose Your Difficulty Level", 
            font=("Arial", 16, "italic"), 
            bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)
    
    # Difficulty buttons with emojis
    btn_easy = tk.Button(root, text="😊 Easy (1-digit numbers)", 
                        font=("Arial", 14, "bold"),
                        width=30, height=2,
                        bg="#90EE90", fg=TEXT_COLOR,
                        activebackground="#7CDB7C",
                        command=lambda: start_quiz(1))
    btn_easy.pack(pady=8)
    
    btn_moderate = tk.Button(root, text="🤔 Moderate (2-digit numbers)", 
                            font=("Arial", 14, "bold"),
                            width=30, height=2,
                            bg="#FFD700", fg=TEXT_COLOR,
                            activebackground="#FFC700",
                            command=lambda: start_quiz(2))
    btn_moderate.pack(pady=8)
    
    btn_advanced = tk.Button(root, text="🔥 Advanced (4-digit numbers)", 
                            font=("Arial", 14, "bold"),
                            width=30, height=2,
                            bg="#FF6B6B", fg=LIGHT_TEXT,
                            activebackground="#FF5252",
                            command=lambda: start_quiz(3))
    btn_advanced.pack(pady=8)
    
    btn_quit = tk.Button(root, text="❌ Quit", 
                        font=("Arial", 12),
                        width=30, height=2,
                        bg="#95a5a6", fg=LIGHT_TEXT,
                        activebackground="#7f8c8d",
                        command=root.destroy)
    btn_quit.pack(pady=20)


def randomInt(level):
    """Return two random integers based on difficulty level."""
    if level == 1:
        return random.randint(1, 9), random.randint(1, 9)
    elif level == 2:
        return random.randint(10, 99), random.randint(10, 99)
    else:
        return random.randint(1000, 9999), random.randint(1000, 9999)


def decideOperation():
    """Randomly decide whether the operation is + or -."""
    return random.choice(['+', '-'])


def displayProblem():
    """Display current arithmetic problem."""
    global num1, num2, operation, answer_entry, attempts

    clear_window()

    # Generate numbers and operation
    num1, num2 = randomInt(difficulty)
    operation = decideOperation()
    attempts = 0

    # Header with progress
    header = tk.Label(root, text=f"📝 Question {question_number}/10", 
                     font=("Comic Sans MS", 18, "bold"), 
                     bg=HEADER_COLOR, fg=LIGHT_TEXT, pady=12)
    header.pack(fill=tk.X)
    
    # Score display
    tk.Label(root, text=f"Current Score: {score}/100", 
            font=("Arial", 14, "bold"), 
            bg=BG_COLOR, fg="#27ae60").pack(pady=15)
    
    # Problem frame with border
    problem_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, borderwidth=3)
    problem_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
    
    tk.Label(problem_frame, text=f"{num1} {operation} {num2} = ?", 
            font=("Arial", 32, "bold"), 
            bg="#ffffff", fg=HEADER_COLOR,
            pady=30).pack()
    
    # Answer entry with styling
    tk.Label(root, text="Enter your answer:", 
            font=("Arial", 12), 
            bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)
    
    answer_entry = tk.Entry(root, font=("Arial", 20), 
                           width=15, justify='center',
                           relief=tk.SOLID, borderwidth=2)
    answer_entry.pack(pady=10)
    answer_entry.focus()
    
    # Bind Enter key to submit
    answer_entry.bind('<Return>', lambda event: check_answer())
    
    # Submit button
    submit_btn = tk.Button(root, text="✓ Submit Answer", 
                          font=("Arial", 14, "bold"),
                          bg=BUTTON_COLOR, fg=LIGHT_TEXT,
                          activebackground=BUTTON_HOVER,
                          width=20, height=2,
                          command=check_answer)
    submit_btn.pack(pady=15)


def isCorrect(user_answer):
    """Check if user's answer is correct."""
    if operation == '+':
        return user_answer == num1 + num2
    else:
        return user_answer == num1 - num2


def check_answer():
    """Handle answer checking and scoring logic."""
    global score, question_number, attempts

    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        messagebox.showerror("⚠️ Invalid Input", "Please enter a valid number!")
        return

    if isCorrect(user_answer):
        if attempts == 0:
            score += 10
            messagebox.showinfo("🎉 Correct!", "Excellent! You got it right!\n+10 points", icon='info')
        else:
            score += 5
            messagebox.showinfo("✓ Correct!", "Good job on second attempt!\n+5 points", icon='info')

        question_number += 1
        if question_number <= 10:
            displayProblem()
        else:
            displayResults()
    else:
        if attempts == 0:
            attempts += 1
            answer_entry.delete(0, tk.END)  # Clear the entry field
            answer_entry.focus()  # Return focus to entry
            messagebox.showwarning("❌ Incorrect", "Oops! Wrong answer.\nTry once more!")
        else:
            correct_ans = num1 + num2 if operation == '+' else num1 - num2
            messagebox.showinfo("😔 Incorrect", 
                              f"Wrong again!\nThe correct answer was:\n{num1} {operation} {num2} = {correct_ans}")
            question_number += 1
            if question_number <= 10:
                displayProblem()
            else:
                displayResults()


def displayResults():
    """Display the final score and ranking."""
    clear_window()

    # Header
    header = tk.Label(root, text="🏆 QUIZ COMPLETE! 🏆", 
                     font=("Comic Sans MS", 22, "bold"), 
                     bg=HEADER_COLOR, fg=LIGHT_TEXT, pady=15)
    header.pack(fill=tk.X)
    
    # Results frame
    results_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, borderwidth=3)
    results_frame.pack(pady=30, padx=40, fill=tk.BOTH, expand=True)
    
    tk.Label(results_frame, text="Your Final Score", 
            font=("Arial", 16), 
            bg="#ffffff", fg=TEXT_COLOR,
            pady=10).pack()
    
    tk.Label(results_frame, text=f"{score}/100", 
            font=("Arial", 48, "bold"), 
            bg="#ffffff", fg="#27ae60",
            pady=5).pack()

    # Grade evaluation with color
    if score >= 90:
        grade = "A+"
        grade_color = "#2ecc71"  # Green
        emoji = "🌟"
    elif score >= 80:
        grade = "A"
        grade_color = "#3498db"  # Blue
        emoji = "⭐"
    elif score >= 70:
        grade = "B"
        grade_color = "#f39c12"  # Orange
        emoji = "👍"
    elif score >= 60:
        grade = "C"
        grade_color = "#e67e22"  # Dark Orange
        emoji = "👌"
    else:
        grade = "F"
        grade_color = "#e74c3c"  # Red
        emoji = "📚"

    tk.Label(results_frame, text=f"{emoji} Grade: {grade} {emoji}", 
            font=("Arial", 28, "bold"), 
            bg="#ffffff", fg=grade_color,
            pady=15).pack()
    
    # Buttons
    btn_again = tk.Button(root, text="🔄 Play Again", 
                         font=("Arial", 14, "bold"),
                         bg=BUTTON_COLOR, fg=LIGHT_TEXT,
                         activebackground=BUTTON_HOVER,
                         width=20, height=2,
                         command=displayMenu)
    btn_again.pack(pady=10)
    
    btn_quit = tk.Button(root, text="❌ Quit", 
                        font=("Arial", 14, "bold"),
                        bg=DANGER_COLOR, fg=LIGHT_TEXT,
                        activebackground="#c9302c",
                        width=20, height=2,
                        command=root.destroy)
    btn_quit.pack(pady=10)


def start_quiz(level):
    """Initialize quiz settings based on difficulty level."""
    global difficulty, score, question_number
    difficulty = level
    score = 0
    question_number = 1
    displayProblem()


def clear_window():
    """Utility function to clear the window."""
    for widget in root.winfo_children():
        widget.destroy()

# -----------------------------
# Main Application Window
# -----------------------------
root = tk.Tk()
root.title("🎯 Arithmetic Quiz Game")
root.geometry("500x550")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

displayMenu()

root.mainloop()
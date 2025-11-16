import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk, ImageSequence  # for GIF animation

# Color Scheme
BG_COLOR = "#ff55ad"  # Light Neon Pink
HEADER_COLOR = "#4a90e2"  # Bright Blue
BUTTON_COLOR = "#5cb85c"  # Success Green
BUTTON_HOVER = "#4cae4c"  # Darker Green
DANGER_COLOR = "#d9534f"  # Red
TEXT_COLOR = "#2c3e50"  # Dark Blue-Gray
LIGHT_TEXT = "#ffffff"  # White


# ----------------------------------------------------------
# START SCREEN (GIF)
# ----------------------------------------------------------

def show_start_screen():
    clear_window()

    global gif_frames, gif_index, gif_label

    gif_frames = []
    gif = Image.open("start screen.gif")  # GIF file

    # Load GIF frames
    for frame in ImageSequence.Iterator(gif):
        frame = frame.resize((500, 550))   # fit window
        gif_frames.append(ImageTk.PhotoImage(frame))

    gif_index = 0

    gif_label = tk.Label(root, bg="black")
    gif_label.pack(fill=tk.BOTH, expand=True)

    animate_gif()

    # ⭐ UPDATED START BUTTON (correct location + correct text)
    start_btn = tk.Button(
        root,
        text="Start",
        font=("Comic Sans MS", 12, "bold"),
        bg="#ff00ff",
        fg="white",
        width=8,
        height=1,
        command=displayMenu
    )

    # ⭐ Position aligned to the "start" area in your GIF
    start_btn.place(relx=0.5, rely=0.75, anchor="center")


def animate_gif():
    global gif_index

    gif_label.config(image=gif_frames[gif_index])
    gif_index = (gif_index + 1) % len(gif_frames)
    root.after(80, animate_gif)  # animation speed


# ----------------------------------------------------------
# MAIN MENU
# ----------------------------------------------------------

def displayMenu():
    """Display difficulty selection menu"""
    clear_window()

    header = tk.Label(root, text="🎯 ARITHMETIC MATHS QUIZ GAME 🎯",
                      font=("Comic Sans MS", 22, "bold"),
                      bg=HEADER_COLOR, fg=LIGHT_TEXT, pady=15)
    header.pack(fill=tk.X)

    tk.Label(root, text="Choose Your Mode That You Want To Play On",
             font=("Arial", 16, "italic"),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

    # Difficulty buttons 
    btn_easy = tk.Button(root, text="😊 Mode Easy (1-digit numbers)",
                         font=("Arial", 14, "bold"),
                         width=30, height=2,
                         bg="#90EE90", fg=TEXT_COLOR,
                         activebackground="#7CDB7C",
                         command=lambda: start_quiz(1))
    btn_easy.pack(pady=8)

    btn_moderate = tk.Button(root, text="🤔 Mode Moderate (2-digit numbers)",
                             font=("Arial", 14, "bold"),
                             width=30, height=2,
                             bg="#FFD700", fg=TEXT_COLOR,
                             activebackground="#FFC700",
                             command=lambda: start_quiz(2))
    btn_moderate.pack(pady=8)

    btn_advanced = tk.Button(root, text="🔥 Mode Advanced (4-digit numbers)",
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


# ----------------------------------------------------------
# QUIZ LOGIC
# ----------------------------------------------------------

def randomInt(level):
    if level == 1:
        return random.randint(1, 9), random.randint(1, 9)
    elif level == 2:
        return random.randint(10, 99), random.randint(10, 99)
    else:
        return random.randint(1000, 9999), random.randint(1000, 9999)


def decideOperation():
    return random.choice(['+', '-'])


def displayProblem():
    global num1, num2, operation, answer_entry, attempts

    clear_window()

    num1, num2 = randomInt(difficulty)
    operation = decideOperation()
    attempts = 0

    header = tk.Label(root, text=f"📝 Question {question_number}/10",
                      font=("Comic Sans MS", 18, "bold"),
                      bg=HEADER_COLOR, fg=LIGHT_TEXT, pady=12)
    header.pack(fill=tk.X)

    tk.Label(root, text=f"Current Score: {score}/100",
             font=("Arial", 14, "bold"),
             bg=BG_COLOR, fg="#27ae60").pack(pady=15)

    problem_frame = tk.Frame(root, bg="#ff55ad", relief=tk.RAISED, borderwidth=3)
    problem_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)

    tk.Label(problem_frame, text=f"{num1} {operation} {num2} = ?",
             font=("Arial", 32, "bold"),
             bg="#ff55ad", fg=HEADER_COLOR,
             pady=30).pack()

    tk.Label(root, text="Enter your answer:",
             font=("Arial", 12),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=5)

    answer_entry = tk.Entry(root, font=("Arial", 20),
                            width=15, justify='center',
                            relief=tk.SOLID, borderwidth=2)
    answer_entry.pack(pady=10)
    answer_entry.focus()

    answer_entry.bind('<Return>', lambda event: check_answer())

    submit_btn = tk.Button(root, text="✓ Submit Answer",
                           font=("Arial", 14, "bold"),
                           bg=BUTTON_COLOR, fg=LIGHT_TEXT,
                           activebackground=BUTTON_HOVER,
                           width=20, height=2,
                           command=check_answer)
    submit_btn.pack(pady=15)


def isCorrect(user_answer):
    return user_answer == (num1 + num2 if operation == '+' else num1 - num2)


def check_answer():
    global score, question_number, attempts

    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        messagebox.showerror("⚠️ Invalid Input", "Please enter a valid number!")
        return

    if isCorrect(user_answer):
        if attempts == 0:
            score += 10
            messagebox.showinfo("🎉 Correct!", "Excellent! You got it right!\n+10 points")
        else:
            score += 5
            messagebox.showinfo("✓ Correct!", "Good job on second attempt!\n+5 points")

        question_number += 1
        if question_number <= 10:
            displayProblem()
        else:
            displayResults()
    else:
        if attempts == 0:
            attempts += 1
            answer_entry.delete(0, tk.END)
            answer_entry.focus()
            messagebox.showwarning("❌ Incorrect", "Oops! Wrong answer.\nTry once more!")
        else:
            correct_ans = num1 + num2 if operation == '+' else num1 - num2
            messagebox.showinfo("😔 Incorrect",
                                f"Wrong again!\nCorrect answer:\n{num1} {operation} {num2} = {correct_ans}")
            question_number += 1

            if question_number <= 10:
                displayProblem()
            else:
                displayResults()


def displayResults():
    clear_window()

    header = tk.Label(root, text="🏆 QUIZ COMPLETED! 🏆",
                      font=("Comic Sans MS", 22, "bold"),
                      bg=HEADER_COLOR, fg=LIGHT_TEXT, pady=15)
    header.pack(fill=tk.X)

    results_frame = tk.Frame(root, bg="#ff55ad", relief=tk.RAISED, borderwidth=3)
    results_frame.pack(pady=30, padx=40, fill=tk.BOTH, expand=True)

    tk.Label(results_frame, text="Your Final Result Is:",
             font=("Arial", 16),
             bg="#ff55ad", fg=TEXT_COLOR,
             pady=10).pack()

    tk.Label(results_frame, text=f"{score}/100",
             font=("Arial", 48, "bold"),
             bg="#ff55ad", fg="#27ae60",
             pady=5).pack()

    if score >= 90:
        grade, grade_color, emoji = "A", "#2ecc71", "🌟"
    elif score >= 80:
        grade, grade_color, emoji = "B", "#3498db", "⭐"
    elif score >= 70:
        grade, grade_color, emoji = "C", "#f39c12", "👍"
    elif score >= 60:
        grade, grade_color, emoji = "D", "#e67e22", "👌"
    else:
        grade, grade_color, emoji = "F", "#e74c3c", "📚"

    tk.Label(results_frame, text=f"{emoji} Grade: {grade} {emoji}",
             font=("Arial", 28, "bold"),
             bg="#ff55ad", fg=grade_color,
             pady=15).pack()

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
    global difficulty, score, question_number
    difficulty = level
    score = 0
    question_number = 1
    displayProblem()


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# ----------------------------------------------------------
# APP WINDOW
# ----------------------------------------------------------

root = tk.Tk()
root.title("🎯 Arithmetic Quiz Game")
root.geometry("500x550")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# Start with GIF page
show_start_screen()

root.mainloop()
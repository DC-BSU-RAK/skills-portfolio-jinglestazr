import tkinter as tk
from tkinter import messagebox
import random
import os

# Color Scheme
BG_COLOR = "#f0f8ff"  # Alice Blue
HEADER_COLOR = "#ff6b9d"  # Pink
BUTTON_COLOR = "#4CAF50"  # Green
BUTTON_HOVER = "#45a049"  # Darker Green
QUIT_COLOR = "#f44336"  # Red
TEXT_COLOR = "#2c3e50"  # Dark Blue-Gray
LIGHT_TEXT = "#ffffff"  # White

class JokeTellingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎭 Alexa - Joke Telling Assistant")
        self.root.geometry("650x550")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        
        self.jokes = []
        self.current_joke = None
        self.load_jokes()
        
        self.create_widgets()
    
    def load_jokes(self):
        """Load jokes from randomJokes.txt file (Format: Setup?Punchline)"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "randomJokes.txt")

            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

                for line in lines:
                    line = line.strip()

                    # Skip empty lines
                    if not line:
                        continue

                    # Must contain at least one question mark
                    if "?" not in line:
                        continue

                    # Split into setup + punchline
                    setup, punchline = line.split("?", 1)
                    setup = setup.strip() + "?"
                    punchline = punchline.strip()

                    self.jokes.append({"setup": setup, "punchline": punchline})

            if not self.jokes:
                messagebox.showerror(
                    "Error",
                    "No valid jokes found in randomJokes.txt.\n\n"
                    "Required format:\nSetup?Punchline"
                )
                self.root.quit()
        
        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                "randomJokes.txt file not found!\n\n"
                "Make sure the file is in the SAME folder as this Python program."
            )
            self.root.quit()

        except Exception as e:
            messagebox.showerror("Error", f"Error loading jokes: {str(e)}")
            self.root.quit()

    def create_widgets(self):
        """Create all GUI widgets"""

        header = tk.Label(
            self.root,
            text="🎭 Alexa - Your Joke Assistant 🎭",
            font=("Comic Sans MS", 22, "bold"),
            bg=HEADER_COLOR,
            fg=LIGHT_TEXT,
            pady=20
        )
        header.pack(fill=tk.X)
        
        self.content_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.content_frame.pack(pady=30, padx=20, fill=tk.BOTH, expand=True)
        
        self.initial_label = tk.Label(
            self.content_frame,
            text="👋 Hello! I'm Alexa, your joke assistant!\n\nClick the button below to hear a joke!",
            font=("Arial", 14, "italic"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            wraplength=550,
            justify=tk.CENTER
        )
        self.initial_label.pack(pady=60)
        
        self.setup_label = tk.Label(
            self.content_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#2980b9",
            wraplength=550,
            relief=tk.RIDGE,
            borderwidth=3,
            padx=25,
            pady=25
        )
        
        self.punchline_label = tk.Label(
            self.content_frame,
            text="",
            font=("Arial", 15, "italic"),
            bg="#fff9e6",
            fg="#e67e22",
            wraplength=550,
            relief=tk.RIDGE,
            borderwidth=3,
            padx=25,
            pady=20
        )
        
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=20)
        
        self.alexa_button = tk.Button(
            button_frame,
            text="🎤 Alexa tell me a Joke",
            font=("Arial", 14, "bold"),
            bg="#9b59b6",
            fg=LIGHT_TEXT,
            activebackground="#8e44ad",
            activeforeground=LIGHT_TEXT,
            width=28,
            height=2,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=3,
            command=self.show_joke_setup
        )
        self.alexa_button.pack(pady=5)
        
        self.punchline_button = tk.Button(
            button_frame,
            text="😄 Show Punchline",
            font=("Arial", 13, "bold"),
            bg="#3498db",
            fg=LIGHT_TEXT,
            activebackground="#2980b9",
            activeforeground=LIGHT_TEXT,
            width=28,
            height=2,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=3,
            command=self.show_punchline
        )
        
        self.next_button = tk.Button(
            button_frame,
            text="➡️ Next Joke",
            font=("Arial", 13, "bold"),
            bg=BUTTON_COLOR,
            fg=LIGHT_TEXT,
            activebackground=BUTTON_HOVER,
            activeforeground=LIGHT_TEXT,
            width=28,
            height=2,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=3,
            command=self.show_joke_setup
        )
        
        quit_button = tk.Button(
            button_frame,
            text="❌ Quit",
            font=("Arial", 12, "bold"),
            bg=QUIT_COLOR,
            fg=LIGHT_TEXT,
            activebackground="#d32f2f",
            activeforeground=LIGHT_TEXT,
            width=28,
            height=2,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=3,
            command=self.quit_app
        )
        quit_button.pack(pady=5)
    
    def show_joke_setup(self):
        if not self.jokes:
            messagebox.showwarning("No Jokes", "No jokes available!")
            return
        
        self.current_joke = random.choice(self.jokes)
        
        self.initial_label.pack_forget()
        self.punchline_label.pack_forget()
        
        self.setup_label.config(text=self.current_joke["setup"])
        self.setup_label.pack(pady=20)
        
        self.alexa_button.pack_forget()
        self.next_button.pack_forget()
        
        self.punchline_button.pack(pady=5)
    
    def show_punchline(self):
        if self.current_joke:
            self.punchline_label.config(text=f"💡 {self.current_joke['punchline']}")
            self.punchline_label.pack(pady=15)
            
            self.punchline_button.pack_forget()
            self.next_button.pack(pady=5)
    
    def quit_app(self):
        if messagebox.askyesno("Quit", "Thanks for laughing with me! 😊\n\nDo you want to quit?"):
            self.root.destroy()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeTellingApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox
import random

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
        self.root.geometry("600x500")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        
        self.jokes = []
        self.current_joke = None
        self.load_jokes()
        
        self.create_widgets()
    
    def load_jokes(self):
        """Load jokes from randomJokes.txt file"""
        try:
            with open("Exercise 2\\randomJokes.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line and line.startswith("-"):
                        # Remove the leading "-" and strip whitespace
                        joke_text = line[1:].strip()
                        # Split by "?" to separate setup and punchline
                        if "?" in joke_text:
                            parts = joke_text.split("?", 1)
                            setup = parts[0].strip() + "?"
                            punchline = parts[1].strip() if len(parts) > 1 else ""
                            self.jokes.append({"setup": setup, "punchline": punchline})
            
            if not self.jokes:
                messagebox.showerror("Error", "No jokes found in randomJokes.txt")
                self.root.quit()
                return
        except FileNotFoundError:
            messagebox.showerror("Error", "randomJokes.txt file not found! Make sure it's in the same folder as this script.")
            self.root.quit()
            return
        except Exception as e:
            messagebox.showerror("Error", f"Error loading jokes: {str(e)}")
            self.root.quit()
            return
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Header
        header = tk.Label(
            self.root,
            text="🎭 Alexa - Your Joke Assistant 🎭",
            font=("Comic Sans MS", 20, "bold"),
            bg=HEADER_COLOR,
            fg=LIGHT_TEXT,
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Main content frame
        self.content_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.content_frame.pack(pady=30, padx=20, fill=tk.BOTH, expand=True)
        
        # Initial message
        self.initial_label = tk.Label(
            self.content_frame,
            text="Click the button below to hear a joke!",
            font=("Arial", 14, "italic"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            wraplength=500
        )
        self.initial_label.pack(pady=40)
        
        # Setup label (hidden initially)
        self.setup_label = tk.Label(
            self.content_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#2980b9",
            wraplength=500,
            relief=tk.RAISED,
            borderwidth=3,
            padx=20,
            pady=20
        )
        
        # Punchline label (hidden initially)
        self.punchline_label = tk.Label(
            self.content_frame,
            text="",
            font=("Arial", 14),
            bg="#fff9e6",
            fg="#e67e22",
            wraplength=500,
            relief=tk.RAISED,
            borderwidth=3,
            padx=20,
            pady=15
        )
        
        # Button frame
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=20)
        
        # "Alexa tell me a Joke" button
        self.alexa_button = tk.Button(
            button_frame,
            text="🎤 Alexa tell me a Joke",
            font=("Arial", 14, "bold"),
            bg="#9b59b6",
            fg=LIGHT_TEXT,
            activebackground="#8e44ad",
            width=25,
            height=2,
            command=self.show_joke_setup
        )
        self.alexa_button.pack(pady=5)
        
        # "Show Punchline" button (hidden initially)
        self.punchline_button = tk.Button(
            button_frame,
            text="😄 Show Punchline",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg=LIGHT_TEXT,
            activebackground="#2980b9",
            width=25,
            height=2,
            command=self.show_punchline
        )
        
        # "Next Joke" button (hidden initially)
        self.next_button = tk.Button(
            button_frame,
            text="➡️ Next Joke",
            font=("Arial", 12, "bold"),
            bg=BUTTON_COLOR,
            fg=LIGHT_TEXT,
            activebackground=BUTTON_HOVER,
            width=25,
            height=2,
            command=self.show_joke_setup
        )
        
        # "Quit" button
        quit_button = tk.Button(
            button_frame,
            text="❌ Quit",
            font=("Arial", 12),
            bg=QUIT_COLOR,
            fg=LIGHT_TEXT,
            activebackground="#d32f2f",
            width=25,
            height=2,
            command=self.root.destroy
        )
        quit_button.pack(pady=5)
    
    def show_joke_setup(self):
        """Display the setup of a random joke"""
        if not self.jokes:
            messagebox.showwarning("No Jokes", "No jokes available!")
            return
        
        # Select a random joke
        self.current_joke = random.choice(self.jokes)
        
        # Hide initial message
        self.initial_label.pack_forget()
        
        # Hide punchline if it was showing
        self.punchline_label.pack_forget()
        
        # Update and show setup
        self.setup_label.config(text=self.current_joke["setup"])
        self.setup_label.pack(pady=20)
        
        # Hide Alexa button and show punchline button
        self.alexa_button.pack_forget()
        self.punchline_button.pack(pady=5)
        
        # Hide next button until punchline is shown
        self.next_button.pack_forget()
    
    def show_punchline(self):
        """Display the punchline of the current joke"""
        if self.current_joke:
            self.punchline_label.config(text=self.current_joke["punchline"])
            self.punchline_label.pack(pady=15)
            
            # Hide punchline button and show next joke button
            self.punchline_button.pack_forget()
            self.next_button.pack(pady=5)


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeTellingApp(root)
    root.mainloop()
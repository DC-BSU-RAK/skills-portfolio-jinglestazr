import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os

# Color Scheme
BG_COLOR = "#f5f5f5"
HEADER_COLOR = "#2c3e50"
BUTTON_COLOR = "#3498db"
BUTTON_HOVER = "#2980b9"
SUCCESS_COLOR = "#27ae60"
WARNING_COLOR = "#e74c3c"
TEXT_COLOR = "#2c3e50"
LIGHT_TEXT = "#ffffff"

class Student:
    """Class to represent a student with their marks"""
    def __init__(self, student_num, name, coursework1, coursework2, coursework3, exam):
        self.student_num = student_num
        self.name = name
        self.coursework1 = int(coursework1)
        self.coursework2 = int(coursework2)
        self.coursework3 = int(coursework3)
        self.exam = int(exam)
    
    def total_coursework(self):
        """Calculate total coursework marks (out of 60)"""
        return self.coursework1 + self.coursework2 + self.coursework3
    
    def overall_percentage(self):
        """Calculate overall percentage (out of 160 total marks)"""
        total = self.total_coursework() + self.exam
        return (total / 160) * 100
    
    def get_grade(self):
        """Determine grade based on percentage"""
        percentage = self.overall_percentage()
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    def format_record(self):
        """Format student record for display"""
        return (f"Student Name: {self.name}\n"
                f"Student Number: {self.student_num}\n"
                f"Total Coursework: {self.total_coursework()}/60\n"
                f"Exam Mark: {self.exam}/100\n"
                f"Overall Percentage: {self.overall_percentage():.2f}%\n"
                f"Grade: {self.get_grade()}\n"
                f"{'-' * 50}")


class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Student Manager System")
        self.root.geometry("900x700")
        self.root.configure(bg=BG_COLOR)
        
        self.students = []
        self.load_students()
        
        self.create_widgets()
    
    def load_students(self):
        """Load student data from studentMarks.txt file"""
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, "studentMarks.txt")
            
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                
                if not lines:
                    messagebox.showerror("Error", "File is empty!")
                    self.root.quit()
                    return
                
                # First line contains number of students
                num_students = int(lines[0].strip())
                
                # Parse each student record
                for i in range(1, num_students + 1):
                    if i < len(lines):
                        line = lines[i].strip()
                        parts = line.split(',')
                        
                        if len(parts) == 6:
                            student_num = parts[0].strip()
                            name = parts[1].strip()
                            cw1 = parts[2].strip()
                            cw2 = parts[3].strip()
                            cw3 = parts[4].strip()
                            exam = parts[5].strip()
                            
                            student = Student(student_num, name, cw1, cw2, cw3, exam)
                            self.students.append(student)
                
                if not self.students:
                    messagebox.showerror("Error", "No valid student records found!")
                    self.root.quit()
                    return
                
                print(f"✅ Successfully loaded {len(self.students)} students!")
                
        except FileNotFoundError:
            messagebox.showerror("Error", 
                f"studentMarks.txt file not found!\n\nMake sure the file is in the same folder as this script.")
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading student data: {str(e)}")
            self.root.quit()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Header
        header = tk.Label(
            self.root,
            text="📚 Student Manager System",
            font=("Arial", 24, "bold"),
            bg=HEADER_COLOR,
            fg=LIGHT_TEXT,
            pady=20
        )
        header.pack(fill=tk.X)
        
        # Info label
        info_label = tk.Label(
            self.root,
            text=f"Total Students: {len(self.students)}",
            font=("Arial", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        info_label.pack(pady=10)
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=20)
        
        # Create buttons
        buttons = [
            ("📋 View All Students", self.view_all_students),
            ("🔍 View Individual Student", self.view_individual_student),
            ("🏆 Highest Score", self.show_highest_score),
            ("⚠️ Lowest Score", self.show_lowest_score),
            ("❌ Exit", self.root.destroy)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 12, "bold"),
                bg=BUTTON_COLOR if "Exit" not in text else WARNING_COLOR,
                fg=LIGHT_TEXT,
                activebackground=BUTTON_HOVER,
                width=25,
                height=2,
                cursor="hand2",
                relief=tk.RAISED,
                borderwidth=3,
                command=command
            )
            btn.pack(pady=5)
        
        # Output Frame with Scrolled Text
        output_frame = tk.LabelFrame(
            self.root,
            text="Output Display",
            font=("Arial", 12, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            relief=tk.GROOVE,
            borderwidth=3
        )
        output_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrolled Text Widget
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            font=("Courier New", 10),
            bg="#ffffff",
            fg=TEXT_COLOR,
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
    
    def display_output(self, text):
        """Display text in the output area"""
        self.clear_output()
        self.output_text.insert(tk.END, text)
    
    def view_all_students(self):
        """Display all student records"""
        output = "=" * 50 + "\n"
        output += "ALL STUDENT RECORDS\n"
        output += "=" * 50 + "\n\n"
        
        total_percentage = 0
        
        for student in self.students:
            output += student.format_record() + "\n"
            total_percentage += student.overall_percentage()
        
        # Summary
        avg_percentage = total_percentage / len(self.students)
        output += "\n" + "=" * 50 + "\n"
        output += "SUMMARY\n"
        output += "=" * 50 + "\n"
        output += f"Total Students: {len(self.students)}\n"
        output += f"Average Percentage: {avg_percentage:.2f}%\n"
        output += "=" * 50 + "\n"
        
        self.display_output(output)
    
    def view_individual_student(self):
        """Display individual student record via selection window"""
        # Create a new window for student selection
        select_window = tk.Toplevel(self.root)
        select_window.title("Select Student")
        select_window.geometry("400x500")
        select_window.configure(bg=BG_COLOR)
        select_window.transient(self.root)
        select_window.grab_set()
        
        # Header
        header = tk.Label(
            select_window,
            text="Select a Student",
            font=("Arial", 16, "bold"),
            bg=HEADER_COLOR,
            fg=LIGHT_TEXT,
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Search frame
        search_frame = tk.Frame(select_window, bg=BG_COLOR)
        search_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(
            search_frame,
            text="Search by Name or Number:",
            font=("Arial", 10),
            bg=BG_COLOR
        ).pack(anchor=tk.W)
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=search_var,
            font=("Arial", 11),
            width=30
        )
        search_entry.pack(fill=tk.X, pady=5)
        
        # Listbox frame
        list_frame = tk.Frame(select_window, bg=BG_COLOR)
        list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        student_listbox = tk.Listbox(
            list_frame,
            font=("Courier New", 10),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        student_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=student_listbox.yview)
        
        # Populate listbox
        def populate_listbox(filter_text=""):
            student_listbox.delete(0, tk.END)
            for idx, student in enumerate(self.students):
                display_text = f"{student.student_num} - {student.name}"
                if filter_text.lower() in display_text.lower():
                    student_listbox.insert(tk.END, display_text)
                    student_listbox.itemconfig(tk.END, {'selectbackground': BUTTON_COLOR})
        
        populate_listbox()
        
        # Search functionality
        def on_search(*args):
            populate_listbox(search_var.get())
        
        search_var.trace('w', on_search)
        
        # View button
        def view_selected():
            selection = student_listbox.curselection()
            if selection:
                selected_text = student_listbox.get(selection[0])
                student_num = selected_text.split(' - ')[0]
                
                for student in self.students:
                    if student.student_num == student_num:
                        output = "=" * 50 + "\n"
                        output += "INDIVIDUAL STUDENT RECORD\n"
                        output += "=" * 50 + "\n\n"
                        output += student.format_record()
                        self.display_output(output)
                        select_window.destroy()
                        return
            else:
                messagebox.showwarning("No Selection", "Please select a student!")
        
        btn_frame = tk.Frame(select_window, bg=BG_COLOR)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="View Record",
            font=("Arial", 11, "bold"),
            bg=SUCCESS_COLOR,
            fg=LIGHT_TEXT,
            width=15,
            command=view_selected
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancel",
            font=("Arial", 11, "bold"),
            bg=WARNING_COLOR,
            fg=LIGHT_TEXT,
            width=15,
            command=select_window.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def show_highest_score(self):
        """Display student with highest overall mark"""
        if not self.students:
            messagebox.showwarning("No Data", "No student records available!")
            return
        
        highest_student = max(self.students, key=lambda s: s.overall_percentage())
        
        output = "=" * 50 + "\n"
        output += "🏆 STUDENT WITH HIGHEST SCORE\n"
        output += "=" * 50 + "\n\n"
        output += highest_student.format_record()
        
        self.display_output(output)
    
    def show_lowest_score(self):
        """Display student with lowest overall mark"""
        if not self.students:
            messagebox.showwarning("No Data", "No student records available!")
            return
        
        lowest_student = min(self.students, key=lambda s: s.overall_percentage())
        
        output = "=" * 50 + "\n"
        output += "⚠️ STUDENT WITH LOWEST SCORE\n"
        output += "=" * 50 + "\n\n"
        output += lowest_student.format_record()
        
        self.display_output(output)


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
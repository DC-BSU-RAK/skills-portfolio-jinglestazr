import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os

# ========== Config ==========
FILE_PATH = "Exercise 3 Extention\studentMarks.txt"  # <-- path to your studentMarks.txt (uploaded file path)
WINDOW_TITLE = "Exercise 3 - Student Manager"

# ========== Utilities ==========
def grade_from_percentage(pct):
    if pct >= 70:
        return "A"
    if pct >= 60:
        return "B"
    if pct >= 50:
        return "C"
    if pct >= 40:
        return "D"
    return "F"

def clamp_int(s, default=0):
    try:
        return int(s)
    except:
        return default

# Student structure: dict with keys:
# 'code' (int), 'name' (str), 'm1' (int), 'm2' (int), 'm3' (int), 'exam' (int)
# computed: 'coursework' (m1+m2+m3), 'total' (coursework+exam), 'percentage' (total/160*100), 'grade'

# ========== File I/O ==========
def load_students_from_file(path=FILE_PATH):
    students = []
    if not os.path.exists(path):
        # create empty file with zero count
        with open(path, "w") as f:
            f.write("0\n")
        return students

    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f.readlines()]

    if not lines:
        return students

    # first line is number of students (we'll ignore mismatch but keep it when saving)
    try:
        count = int(lines[0].strip())
    except:
        count = None

    for ln in lines[1:]:
        if not ln.strip():
            continue
        parts = [p.strip() for p in ln.split(",")]
        if len(parts) < 6:
            # invalid line - skip
            continue
        code = clamp_int(parts[0], None)
        name = parts[1]
        m1 = clamp_int(parts[2], 0)
        m2 = clamp_int(parts[3], 0)
        m3 = clamp_int(parts[4], 0)
        exam = clamp_int(parts[5], 0)

        coursework = m1 + m2 + m3
        total = coursework + exam
        percentage = (total / 160.0) * 100.0 if total is not None else 0.0
        grade = grade_from_percentage(percentage)

        students.append({
            "code": code,
            "name": name,
            "m1": m1,
            "m2": m2,
            "m3": m3,
            "exam": exam,
            "coursework": coursework,
            "total": total,
            "percentage": percentage,
            "grade": grade
        })
    return students

def save_students_to_file(students, path=FILE_PATH):
    # First line must be number of students
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(len(students)) + "\n")
            for s in students:
                # Write in required format: code,name,m1,m2,m3,exam
                f.write(f"{s['code']},{s['name']},{s['m1']},{s['m2']},{s['m3']},{s['exam']}\n")
        return True
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save to file:\n{str(e)}")
        return False

# ========== GUI Application ==========
class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry("850x600")

        # Data
        self.students = load_students_from_file()

        # Top frame: buttons / menu
        top_frame = tk.Frame(root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)

        btn_specs = [
            ("1. View all records", self.view_all_records),
            ("2. View individual record", self.view_individual_record),
            ("3. Show highest overall", self.show_highest_overall),
            ("4. Show lowest overall", self.show_lowest_overall),
            ("5. Sort records", self.sort_records),
            ("6. Add record", self.add_record),
            ("7. Delete record", self.delete_record),
            ("8. Update record", self.update_record),
            ("Reload file", self.reload_from_file),
            ("Save to file", self.save_to_file),
        ]

        for (text, cmd) in btn_specs:
            b = tk.Button(top_frame, text=text, command=cmd, width=18)
            b.pack(side=tk.LEFT, padx=4)

        # Middle: output text area with scrollbar
        middle_frame = tk.Frame(root)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        self.output_text = tk.Text(middle_frame, wrap=tk.WORD, font=("Consolas", 11))
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(middle_frame, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)

        # Footer: status
        footer = tk.Frame(root)
        footer.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=6)
        self.status_label = tk.Label(footer, text=f"Loaded {len(self.students)} students from {FILE_PATH}")
        self.status_label.pack(side=tk.LEFT)

        # Initial message
        self.print_line("Student Manager ready. Click a button to operate.")
        self.print_line(f"Data file: {FILE_PATH}")
        self.print_line("")

    # ---------- Helpers ----------
    def print_line(self, s=""):
        self.output_text.insert(tk.END, str(s) + "\n")
        self.output_text.see(tk.END)

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

    def refresh_status(self):
        self.status_label.config(text=f"Loaded {len(self.students)} students from {FILE_PATH}")

    def recalc_student(self, s):
        s["coursework"] = s["m1"] + s["m2"] + s["m3"]
        s["total"] = s["coursework"] + s["exam"]
        s["percentage"] = (s["total"] / 160.0) * 100.0
        s["grade"] = grade_from_percentage(s["percentage"])

    def find_student_by_code_or_name(self, key):
        key = key.strip().lower()
        matches = []
        for s in self.students:
            if s["code"] is not None and str(s["code"]) == key:
                matches.append(s)
            elif key in s["name"].lower():
                matches.append(s)
        return matches

    def format_student_for_output(self, s):
        out = []
        out.append(f"Name: {s['name']}")
        out.append(f"Student Number: {s['code']}")
        out.append(f"Total coursework mark (out of 60): {s['coursework']}")
        out.append(f"Exam mark (out of 100): {s['exam']}")
        out.append(f"Overall percentage (out of 160): {s['percentage']:.2f}%")
        out.append(f"Student grade: {s['grade']}")
        return "\n".join(out)

    # ---------- Menu Item Implementations ----------
    def view_all_records(self):
        self.clear_output()
        if not self.students:
            self.print_line("No students loaded.")
            return

        self.print_line("=== ALL STUDENT RECORDS ===\n")
        total_pct_sum = 0.0
        for s in self.students:
            self.print_line(self.format_student_for_output(s))
            self.print_line("-" * 60)
            total_pct_sum += s["percentage"]

        avg_pct = (total_pct_sum / len(self.students)) if self.students else 0.0
        self.print_line(f"\nNumber of students: {len(self.students)}")
        self.print_line(f"Average percentage mark: {avg_pct:.2f}%")
        self.print_line("")

    def view_individual_record(self):
        if not self.students:
            messagebox.showinfo("No data", "No students loaded.")
            return

        key = simpledialog.askstring("Find Student", "Enter student code or name (partial name allowed):")
        if key is None:
            return
        matches = self.find_student_by_code_or_name(key)
        self.clear_output()

        if not matches:
            self.print_line("No students matched your search.")
            return

        if len(matches) == 1:
            s = matches[0]
            self.print_line("=== STUDENT RECORD ===")
            self.print_line(self.format_student_for_output(s))
        else:
            self.print_line(f"Found {len(matches)} matches. Showing all results:\n")
            for s in matches:
                self.print_line(self.format_student_for_output(s))
                self.print_line("-" * 50)

    def show_highest_overall(self):
        if not self.students:
            messagebox.showinfo("No data", "No students loaded.")
            return
        best = max(self.students, key=lambda x: x["percentage"])
        self.clear_output()
        self.print_line("=== HIGHEST OVERALL MARK ===\n")
        self.print_line(self.format_student_for_output(best))
        self.print_line("")

    def show_lowest_overall(self):
        if not self.students:
            messagebox.showinfo("No data", "No students loaded.")
            return
        worst = min(self.students, key=lambda x: x["percentage"])
        self.clear_output()
        self.print_line("=== LOWEST OVERALL MARK ===\n")
        self.print_line(self.format_student_for_output(worst))
        self.print_line("")

    def sort_records(self):
        if not self.students:
            messagebox.showinfo("No data", "No students loaded.")
            return

        # Simple dialogs to choose sort field and order
        field = simpledialog.askstring("Sort", "Sort by (code/name/coursework/percentage/grade):", initialvalue="percentage")
        if field is None:
            return
        field = field.strip().lower()
        if field not in ("code", "name", "coursework", "percentage", "grade", "total"):
            messagebox.showerror("Invalid", "Invalid sort field.")
            return

        order = simpledialog.askstring("Order", "Order (A)scending or (D)escending:", initialvalue="D")
        if order is None:
            return
        desc = (order.strip().lower() == "d")

        # Sorting key
        if field in ("coursework", "percentage", "total", "code"):
            self.students.sort(key=lambda s: (s[field] if s[field] is not None else 0), reverse=desc)
        else:  # name or grade
            self.students.sort(key=lambda s: s[field].lower(), reverse=desc)

        self.clear_output()
        self.print_line(f"Records sorted by {field} {'descending' if desc else 'ascending'}:\n")
        self.view_all_records()

    def add_record(self):
        # ask user for each field
        code = simpledialog.askstring("Add Student", "Enter student code (1000-9999):")
        if code is None:
            return
        try:
            code_int = int(code)
            if not (1000 <= code_int <= 9999):
                messagebox.showerror("Invalid code", "Student code must be between 1000 and 9999.")
                return
        except:
            messagebox.showerror("Invalid", "Student code must be numeric.")
            return

        # check duplicates
        for s in self.students:
            if s["code"] == code_int:
                if not messagebox.askyesno("Duplicate", f"Student code {code_int} already exists. Add anyway?"):
                    return
                break

        name = simpledialog.askstring("Add Student", "Enter student full name:")
        if name is None or not name.strip():
            messagebox.showerror("Invalid", "Name cannot be empty.")
            return

        def ask_mark(prompt, maxv):
            while True:
                val = simpledialog.askstring("Add Student", prompt)
                if val is None:
                    return None
                try:
                    iv = int(val)
                    if 0 <= iv <= maxv:
                        return iv
                    else:
                        messagebox.showerror("Invalid", f"Please enter an integer between 0 and {maxv}.")
                except:
                    messagebox.showerror("Invalid", "Please enter a valid integer.")

        m1 = ask_mark("Enter coursework mark 1 (out of 20):", 20)
        if m1 is None: return
        m2 = ask_mark("Enter coursework mark 2 (out of 20):", 20)
        if m2 is None: return
        m3 = ask_mark("Enter coursework mark 3 (out of 20):", 20)
        if m3 is None: return
        exam = ask_mark("Enter exam mark (out of 100):", 100)
        if exam is None: return

        new_s = {
            "code": code_int,
            "name": name.strip(),
            "m1": m1,
            "m2": m2,
            "m3": m3,
            "exam": exam
        }
        self.recalc_student(new_s)
        self.students.append(new_s)
        saved = save_students_to_file(self.students)
        if saved:
            messagebox.showinfo("Added", "Student added and file updated.")
            self.refresh_status()
            self.clear_output()
            self.print_line("Added student:")
            self.print_line(self.format_student_for_output(new_s))
        else:
            messagebox.showerror("Error", "Could not save new student to file.")

    def delete_record(self):
        if not self.students:
            messagebox.showinfo("No data", "No students loaded.")
            return
        key = simpledialog.askstring("Delete Student", "Enter student code or name to delete (partial name OK):")
        if key is None:
            return
        matches = self.find_student_by_code_or_name(key)
        if not matches:
            messagebox.showinfo("Not found", "No matching student found.")
            return

        if len(matches) == 1:
            s = matches[0]
            confirm = messagebox.askyesno("Confirm Delete", f"Delete {s['name']} ({s['code']})?")
            if confirm:
                self.students.remove(s)
                save_students_to_file(self.students)
                self.refresh_status()
                messagebox.showinfo("Deleted", f"Deleted {s['name']}.")
        else:
            # multiple matches - show them and ask which code to delete
            pick_text = "Multiple matches found:\n\n"
            for idx, s in enumerate(matches, start=1):
                pick_text += f"{idx}. {s['name']} ({s['code']})\n"
            pick_text += "\nEnter the NUMBER of the record to delete (or Cancel):"
            choice = simpledialog.askstring("Delete Student", pick_text)
            if choice is None:
                return
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(matches):
                    target = matches[choice_idx]
                    confirm = messagebox.askyesno("Confirm Delete", f"Delete {target['name']} ({target['code']})?")
                    if confirm:
                        self.students.remove(target)
                        save_students_to_file(self.students)
                        self.refresh_status()
                        messagebox.showinfo("Deleted", f"Deleted {target['name']}.")
                else:
                    messagebox.showerror("Invalid", "Selection out of range.")
            except:
                messagebox.showerror("Invalid", "Please enter a valid number.")

    def update_record(self):
        if not self.students:
            messagebox.showinfo("No data", "No students loaded.")
            return
        key = simpledialog.askstring("Update Student", "Enter student code or name to update (partial name OK):")
        if key is None:
            return
        matches = self.find_student_by_code_or_name(key)
        if not matches:
            messagebox.showinfo("Not found", "No matching student found.")
            return

        if len(matches) > 1:
            pick_text = "Multiple matches found:\n\n"
            for idx, s in enumerate(matches, start=1):
                pick_text += f"{idx}. {s['name']} ({s['code']})\n"
            pick_text += "\nEnter the NUMBER of the record to update (or Cancel):"
            choice = simpledialog.askstring("Update Student", pick_text)
            if choice is None:
                return
            try:
                idx = int(choice) - 1
                if not (0 <= idx < len(matches)):
                    messagebox.showerror("Invalid", "Selection out of range.")
                    return
                student = matches[idx]
            except:
                messagebox.showerror("Invalid", "Enter a valid number.")
                return
        else:
            student = matches[0]

        # Sub-menu for update
        while True:
            opt = simpledialog.askstring("Update Menu",
                f"Updating {student['name']} ({student['code']})\n\n"
                "Choose field to update:\n"
                "1. Name\n2. Student code\n3. Coursework mark 1\n4. Coursework mark 2\n5. Coursework mark 3\n6. Exam mark\n7. Done\n\nEnter choice number:")
            if opt is None:
                return
            opt = opt.strip()
            if opt == "1":
                newname = simpledialog.askstring("Update", "Enter new full name:", initialvalue=student['name'])
                if newname:
                    student['name'] = newname.strip()
            elif opt == "2":
                newcode = simpledialog.askstring("Update", "Enter new student code (1000-9999):", initialvalue=str(student['code']))
                if newcode:
                    try:
                        nc = int(newcode)
                        if 1000 <= nc <= 9999:
                            student['code'] = nc
                        else:
                            messagebox.showerror("Invalid", "Code must be between 1000 and 9999.")
                    except:
                        messagebox.showerror("Invalid", "Enter a numeric code.")
            elif opt == "3":
                val = simpledialog.askstring("Update", "Enter coursework mark 1 (0-20):", initialvalue=str(student['m1']))
                if val is not None:
                    try:
                        v = int(val)
                        if 0 <= v <= 20:
                            student['m1'] = v
                        else:
                            messagebox.showerror("Invalid", "Enter 0-20.")
                    except:
                        messagebox.showerror("Invalid", "Enter an integer.")
            elif opt == "4":
                val = simpledialog.askstring("Update", "Enter coursework mark 2 (0-20):", initialvalue=str(student['m2']))
                if val is not None:
                    try:
                        v = int(val)
                        if 0 <= v <= 20:
                            student['m2'] = v
                        else:
                            messagebox.showerror("Invalid", "Enter 0-20.")
                    except:
                        messagebox.showerror("Invalid", "Enter an integer.")
            elif opt == "5":
                val = simpledialog.askstring("Update", "Enter coursework mark 3 (0-20):", initialvalue=str(student['m3']))
                if val is not None:
                    try:
                        v = int(val)
                        if 0 <= v <= 20:
                            student['m3'] = v
                        else:
                            messagebox.showerror("Invalid", "Enter 0-20.")
                    except:
                        messagebox.showerror("Invalid", "Enter an integer.")
            elif opt == "6":
                val = simpledialog.askstring("Update", "Enter exam mark (0-100):", initialvalue=str(student['exam']))
                if val is not None:
                    try:
                        v = int(val)
                        if 0 <= v <= 100:
                            student['exam'] = v
                        else:
                            messagebox.showerror("Invalid", "Enter 0-100.")
                    except:
                        messagebox.showerror("Invalid", "Enter an integer.")
            elif opt == "7":
                break
            else:
                messagebox.showerror("Invalid", "Choose 1-7.")

            # Recalculate after each change
            self.recalc_student(student)

        # Save changes
        saved = save_students_to_file(self.students)
        if saved:
            messagebox.showinfo("Updated", "Student record updated and file saved.")
            self.refresh_status()
        else:
            messagebox.showerror("Error", "Failed to save updates to file.")

    # ---------- File / reload ----------
    def reload_from_file(self):
        self.students = load_students_from_file()
        self.refresh_status()
        messagebox.showinfo("Reloaded", "Data reloaded from file.")

    def save_to_file(self):
        saved = save_students_to_file(self.students)
        if saved:
            messagebox.showinfo("Saved", "Data saved to file.")
            self.refresh_status()
        else:
            messagebox.showerror("Error", "Failed to save data to file.")


# ========== Run Application ==========
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
1
"""
Features:
1. View all student records
2. View individual student record
3. Highest overall score
4. Lowest overall score
5. Sort records
6. Add student
7. Delete student
8. Update student
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

DATA_FILE = r"Exercise 3 Extention\studentMarks.txt"


def to_int(x, default=0):
    try:
        return int(x)
    except:
        return default

def grade_from_percentage(p):
    if p >= 70: return "A"
    if p >= 60: return "B"
    if p >= 50: return "C"
    if p >= 40: return "D"
    return "F"

def recalc(s):
    s['coursework'] = s['m1'] + s['m2'] + s['m3']
    s['total'] = s['coursework'] + s['exam']
    s['percentage'] = (s['total'] / 160.0) * 100
    s['grade'] = grade_from_percentage(s['percentage'])


def load_students(path=DATA_FILE):
    students = []
    if not os.path.exists(path):
        # ensure folder exists if path contains dirs (optional)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path,"w", encoding="utf-8") as f:
            f.write("0\n")
        return students

    with open(path,"r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines()]

    for ln in lines[1:]:
        if not ln: continue
        parts = ln.split(",")
        if len(parts) < 6: continue
        code = to_int(parts[0], None)
        name = parts[1]
        m1 = to_int(parts[2])
        m2 = to_int(parts[3])
        m3 = to_int(parts[4])
        exam = to_int(parts[5])
        s = {"code": code, "name": name, "m1": m1, "m2": m2, "m3": m3, "exam": exam}
        recalc(s)
        students.append(s)
    return students

def save_students(students, path=DATA_FILE):
    try:
        # ensure parent folder exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path,"w", encoding="utf-8") as f:
            f.write(str(len(students)) + "\n")
            for s in students:
                f.write(f"{s['code']},{s['name']},{s['m1']},{s['m2']},{s['m3']},{s['exam']}\n")
        return True
    except Exception as e:
        messagebox.showerror("Save error", f"Failed to save file:\n{e}")
        return False


class StudentManager:
    def __init__(self, root):
        self.root = root
        root.title("Student Manager (Full Screen Mode)")
        root.geometry("900x600")

        self.students = load_students()

        # LEFT BUTTONS FRAME
        left = tk.Frame(root, width=220, padx=8, pady=8, bg="#E5CFE6")
        left.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(left, text="Student Manager", font=("Helvetica", 14, "bold"), bg="#d900ff").pack(pady=(0,10))

        btn_cfg = {"width":22, "pady":4}
        tk.Button(left, text="1. View all records",   command=self.view_all,   **btn_cfg).pack()
        tk.Button(left, text="2. View individual",    command=self.show_individual_form, **btn_cfg).pack()
        tk.Button(left, text="3. Highest overall",    command=self.highest,   **btn_cfg).pack()
        tk.Button(left, text="4. Lowest overall",     command=self.lowest,    **btn_cfg).pack()
        tk.Button(left, text="5. Sort records",       command=self.show_sort_form, **btn_cfg).pack()
        tk.Button(left, text="6. Add record",         command=self.show_add_form, **btn_cfg).pack()
        tk.Button(left, text="7. Delete record",      command=self.show_delete_form, **btn_cfg).pack()
        tk.Button(left, text="8. Update record",      command=self.show_update_form, **btn_cfg).pack()
        tk.Button(left, text="Reload file",           command=self.reload,    **btn_cfg).pack(pady=(8,0))
        tk.Button(left, text="Save to file",          command=self.save,      **btn_cfg).pack()

        # CENTER TEXT OUTPUT AREA
        center = tk.Frame(root, padx=6, pady=6, bg="#030450")
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(center, text="Details / Output:", font=("Helvetica", 12, "bold"), bg="#030450").pack(anchor="w")

        self.txt = tk.Text(center, wrap=tk.WORD, bg="#BCF9FF")
        self.txt.pack(fill=tk.BOTH, expand=True)

        # BOTTOM FORM AREA (Hidden until needed)
        self.form_area = tk.Frame(root, padx=8, pady=8, bg="#E5CFE6")
        self.form_area.pack(side=tk.BOTTOM, fill=tk.X)
        self.clear_form()

        self.log("Loaded {} students.".format(len(self.students)))
        self.view_all()


    def log(self, text):
        self.txt.insert(tk.END, text + "\n")
        self.txt.see(tk.END)

    def clear_form(self):
        for w in self.form_area.winfo_children():
            w.destroy()
        self.form_area.pack_forget()

    def show_form(self):
        self.form_area.pack(side=tk.BOTTOM, fill=tk.X)

    def format_student(self, s):
        return (f"Name: {s['name']}\n"
                f"Student Number: {s['code']}\n"
                f"Coursework (out of 60): {s['coursework']}\n"
                f"Exam (out of 100): {s['exam']}\n"
                f"Total /160: {s['total']}\n"
                f"Percentage: {s['percentage']:.2f}%  Grade: {s['grade']}")

    def find_matches(self, key):
        key = (key or "").lower().strip()
        matches = []
        for s in self.students:
            if s['code'] is not None and str(s['code']) == key:
                matches.append(s)
            elif key in s['name'].lower():
                matches.append(s)
        return matches

    # Menu Functions 
    def view_all(self):
        self.clear_form()
        self.txt.delete(1.0, tk.END)
        if not self.students:
            self.log("No students loaded.")
            return
        tot = 0
        for s in self.students:
            self.log(self.format_student(s))
            self.log("-"*40)
            tot += s['percentage']
        avg = tot / len(self.students) if self.students else 0.0
        self.log(f"Number of students: {len(self.students)}")
        self.log(f"Average percentage: {avg:.2f}%")

    def highest(self):
        self.clear_form()
        if not self.students:
            messagebox.showinfo("No data", "No students loaded.")
            return
        top = max(self.students, key=lambda x: x['percentage'])
        self.txt.delete(1.0, tk.END)
        self.log("=== HIGHEST OVERALL ===")
        self.log(self.format_student(top))

    def lowest(self):
        self.clear_form()
        if not self.students:
            messagebox.showinfo("No data", "No students loaded.")
            return
        low = min(self.students, key=lambda x: x['percentage'])
        self.txt.delete(1.0, tk.END)
        self.log("=== LOWEST OVERALL ===")
        self.log(self.format_student(low))

    # Individual Search 
    def show_individual_form(self):
        self.clear_form()
        self.show_form()

        tk.Label(self.form_area, text="Enter code or name:", bg="#E5CFE6").grid(row=0, column=0, sticky="w")
        entry = tk.Entry(self.form_area, width=40)
        entry.grid(row=0, column=1)

        def do_search():
            key = entry.get().strip()
            self.txt.delete(1.0, tk.END)
            if not key:
                self.log("Enter something to search.")
                return
            matches = self.find_matches(key)
            if not matches:
                self.log("No matches found.")
                return
            for s in matches:
                self.log(self.format_student(s))
                self.log("-"*40)

        tk.Button(self.form_area, text="Find", command=do_search).grid(row=0, column=2, padx=6)
        tk.Button(self.form_area, text="Cancel", command=self.clear_form).grid(row=0, column=3, padx=6)

    # Sorting 
    def show_sort_form(self):
        self.clear_form()
        self.show_form()

        tk.Label(self.form_area, text="Sort field:").grid(row=0, column=0)
        field = tk.Entry(self.form_area, width=20)
        field.grid(row=0, column=1)
        field.insert(0, "percentage")

        tk.Label(self.form_area, text="Order (A/D):").grid(row=1, column=0)
        order = tk.Entry(self.form_area, width=5)
        order.grid(row=1, column=1)
        order.insert(0, "D")

        def do_sort():
            f = field.get().strip().lower()
            o = order.get().strip().lower()
            if f not in ("code","name","coursework","percentage","grade","total"):
                messagebox.showerror("Invalid", "Invalid sort field.")
                return
            desc = (o == "d")
            if f in ("coursework","percentage","total","code"):
                self.students.sort(key=lambda s: s[f], reverse=desc)
            else:
                self.students.sort(key=lambda s: s[f].lower(), reverse=desc)
            self.view_all()
            messagebox.showinfo("Sorted", "Records sorted.")
            self.clear_form()

        tk.Button(self.form_area, text="Sort", command=do_sort).grid(row=2, column=0, pady=6)
        tk.Button(self.form_area, text="Cancel", command=self.clear_form).grid(row=2, column=1, pady=6)

    # Adding Student
    def show_add_form(self):
        self.clear_form()
        self.show_form()

        # Explanation of code names of marks to the user 
        explain = tk.Label(
            self.form_area,
            text="Marks breakdown:\n"
                 "m1 = Course Mark 1 (20%)\n"
                 "m2 = Course Mark 2 (20%)\n"
                 "m3 = Course Mark 3 (20%)\n"
                 "Exam = Final Examination Marks (100)",
            justify="left",
            font=("Helvetica", 9)
        )
        explain.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,10))

        # Entry fields
        labels = ["Code (1000-9999)", "Name", "m1 (0-20)", "m2 (0-20)", "m3 (0-20)", "Exam (0-100)"]
        entries = []

        for i, l in enumerate(labels):
            tk.Label(self.form_area, text=l).grid(row=i+1, column=0, sticky="w")
            e = tk.Entry(self.form_area, width=35)
            e.grid(row=i+1, column=1)
            entries.append(e)

        def do_add():
            try:
                code = int(entries[0].get())
            except:
                messagebox.showerror("Invalid", "Code must be a number.")
                return
            if not (1000 <= code <= 9999):
                messagebox.showerror("Invalid", "Code must be 1000-9999.")
                return

            name = entries[1].get().strip()
            if not name:
                messagebox.showerror("Invalid", "Name required.")
                return

            try:
                m1 = int(entries[2].get()); m2 = int(entries[3].get())
                m3 = int(entries[4].get()); exam = int(entries[5].get())
            except:
                messagebox.showerror("Invalid", "Marks must be integers.")
                return

            if not all(0 <= v <= 20 for v in (m1,m2,m3)) or not (0 <= exam <= 100):
                messagebox.showerror("Invalid", "Marks out of range.")
                return

            new = {"code": code, "name": name, "m1": m1, "m2": m2, "m3": m3, "exam": exam}
            recalc(new)

            self.students.append(new)
            save_students(self.students)

            messagebox.showinfo("Added", "Student added.")
            self.view_all()
            self.clear_form()

        tk.Button(self.form_area, text="Add", command=do_add).grid(row=len(labels)+2, column=0, pady=6)
        tk.Button(self.form_area, text="Cancel", command=self.clear_form).grid(row=len(labels)+2, column=1, pady=6)

    # Delete Student 
    def show_delete_form(self):
        self.clear_form()
        self.show_form()

        tk.Label(self.form_area, text="Code or name to delete:").grid(row=0, column=0)
        entry = tk.Entry(self.form_area, width=40)
        entry.grid(row=0, column=1)

        def do_find():
            key = entry.get().strip()
            matches = self.find_matches(key)
            self.txt.delete(1.0, tk.END)

            if not matches:
                self.log("No matches.")
                return

            if len(matches) == 1:
                s = matches[0]
                self.log("Found: ")
                self.log(self.format_student(s))
                if messagebox.askyesno("Confirm", f"Delete {s['name']}?"):
                    self.students.remove(s)
                    save_students(self.students)
                    self.view_all()
                    self.clear_form()
                return

            self.log("Multiple matches:")
            for i,s in enumerate(matches, start=1):
                self.log(f"{i}. {s['name']} ({s['code']})")

            tk.Label(self.form_area, text="Enter number:").grid(row=1, column=0)
            idx_entry = tk.Entry(self.form_area, width=5)
            idx_entry.grid(row=1, column=1)

            def do_delete():
                try:
                    idx = int(idx_entry.get()) - 1
                except:
                    messagebox.showerror("Invalid", "Enter a number.")
                    return
                if 0 <= idx < len(matches):
                    s = matches[idx]
                    if messagebox.askyesno("Confirm", f"Delete {s['name']}?"):
                        self.students.remove(s)
                        save_students(self.students)
                        self.view_all()
                        self.clear_form()
                else:
                    messagebox.showerror("Invalid", "Index out of range.")

            tk.Button(self.form_area, text="Delete", command=do_delete).grid(row=1, column=2)

        tk.Button(self.form_area, text="Find", command=do_find).grid(row=0, column=2)
        tk.Button(self.form_area, text="Cancel", command=self.clear_form).grid(row=0, column=3)

    # Update Student 
    def show_update_form(self):
        self.clear_form()
        self.show_form()

        tk.Label(self.form_area, text="Code or name to update:").grid(row=0, column=0)
        search = tk.Entry(self.form_area, width=40)
        search.grid(row=0, column=1)

        def do_find():
            key = search.get().strip()
            matches = self.find_matches(key)
            self.txt.delete(1.0, tk.END)

            if not matches:
                self.log("No matches.")
                return

            if len(matches) > 1:
                self.log("Multiple matches:")
                for i,s in enumerate(matches, start=1):
                    self.log(f"{i}. {s['name']} ({s['code']})")

                tk.Label(self.form_area, text="Enter number:").grid(row=1, column=0)
                idx_entry = tk.Entry(self.form_area, width=5)
                idx_entry.grid(row=1, column=1)

                def select():
                    try:
                        idx = int(idx_entry.get()) - 1
                    except:
                        messagebox.showerror("Invalid", "Enter a number.")
                        return
                    if 0 <= idx < len(matches):
                        show_edit_form(matches[idx])
                    else:
                        messagebox.showerror("Invalid", "Index out of range.")
                tk.Button(self.form_area, text="Select", command=select).grid(row=1, column=2)
                return

            show_edit_form(matches[0])

        def show_edit_form(student):
            # remove previous edit widgets (rows >= 2)
            for w in self.form_area.grid_slaves():
                if int(w.grid_info()["row"]) >= 2:
                    w.grid_forget()

            labels = ["Name", "Code (1000-9999)", "m1 (0-20)", "m2 (0-20)", "m3 (0-20)", "Exam (0-100)"]
            entries = []

            initial = [student['name'], student['code'], student['m1'], student['m2'], student['m3'], student['exam']]

            for i,l in enumerate(labels):
                tk.Label(self.form_area, text=l).grid(row=2+i, column=0, sticky="w")
                e = tk.Entry(self.form_area, width=35)
                e.grid(row=2+i, column=1)
                e.insert(0, str(initial[i]))
                entries.append(e)

            def do_update():
                name = entries[0].get().strip()
                try:
                    code = int(entries[1].get())
                    m1 = int(entries[2].get())
                    m2 = int(entries[3].get())
                    m3 = int(entries[4].get())
                    exam = int(entries[5].get())
                except:
                    messagebox.showerror("Invalid", "All fields must be valid integers.")
                    return
                if not (1000 <= code <= 9999):
                    messagebox.showerror("Invalid", "Code must be 1000-9999.")
                    return
                if not all(0 <= v <= 20 for v in (m1,m2,m3)) or not (0 <= exam <= 100):
                    messagebox.showerror("Invalid", "Marks out of range.")
                    return

                student['name'] = name
                student['code'] = code
                student['m1'] = m1
                student['m2'] = m2
                student['m3'] = m3
                student['exam'] = exam
                recalc(student)

                save_students(self.students)
                messagebox.showinfo("Updated", "Student updated.")
                self.view_all()
                self.clear_form()

            tk.Button(self.form_area, text="Save", command=do_update).grid(row=2+len(labels), column=0, pady=6)
            tk.Button(self.form_area, text="Cancel", command=self.clear_form).grid(row=2+len(labels), column=1, pady=6)

        tk.Button(self.form_area, text="Find", command=do_find).grid(row=0, column=2)
        tk.Button(self.form_area, text="Cancel", command=self.clear_form).grid(row=0, column=3)

    # File 
    def reload(self):
        self.students = load_students()
        self.view_all()
        messagebox.showinfo("Reloaded", "File reloaded.")

    def save(self):
        if save_students(self.students):
            messagebox.showinfo("Saved", "File saved.")
        else:
            messagebox.showerror("Error", "Failed to save file.")


#Runnig the App
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#E5CFE6") 

    app = StudentManager(root)
    root.mainloop()

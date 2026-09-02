"""RoboGUI 1.2.1 - Copy only newer files.
Copyright (C) 2025-2026  SymbolForm

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import tkinter as tk
from tkinter import Label, Button, Entry, messagebox
import tkinter.ttk as ttk

# Base64 placeholder icons (replace or expand as needed)
img = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAZxJREFUWIXt179rFkEQxvHPmICK6V4htipoGdTGRhQFSxWE/AdBS0sFwdrK0iog1jb2CoKClfgDU4gWKiRNCIIQBJGMzasEcvdm9/JeXgsfmOZ2dua7MztwG5lpktoz0eyYbluIiAHOYVAR7wceZ+b34h2ZucVwCqvIDvYGg6a4TRZNdyAinuEs7uNLRQXO4yLe4kJmrnWtwCpWSk+xad/12kq0XcIp/Kw4eZPm8DQiDo5y6nsK5vBkFMRujOEfiMZpah3DjnqBd5jZ9G3fEGIRV3oFyMz3w2R/FRHTWMfxpj29tyAzf2Gjbb2oAhFxCJdq8uJRZn7bzrG0BTM4jCj038B+jAcgMz/hVmHyKpW24CRuVsRN3M7Mj2MBwAfcrQCAryVOpS1Yx6tKgCKVtuAMHlTETVzOzKWxAGTmcxytAChWaQUO4LT2Mfw8nJR+AHAM10asv8S93gAy8zXmuyTYThP/K/4P8M8CrGE2Io7sNEFEnMDeYcytavm9vqPbo2SULdQ8TKZwA1cxu8MiLOMhFrMhWSPAbmril/A3Lo8hMwXmrDcAAAAASUVORK5CYII='

folder = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAXpJREFUWIXtl7FKA0EQhr/RRBAxoAhaWYr4CCIWinkCURBLC3sLwcbawk4QwS6VvoE2PoBWFloEhEAsBEUQUUTP3+L2wpFccvE8uRQ3MNwycPt/uzvDzpoksrS+TNV7AaDQHDCzOWCaaLhX4FJSNTUCSQ0HKoBi3AP2gUL436RuQRKaWRk4A66AYyfWbEPAJjAFnADrkr5S2QFgy4mudiIGRhykHETxLzsQzoFg7MUAP5vZEnAOrACzZvbQxVq/gRtgV1Itage23aqWuyEHSvhH9Uh83oS9BpSCeRKXoaQXSRuSxiRZnONX1QEwCZSDeVrKEBg1s3lgIClcG/sAgvKd6ARwlLJwR4sCqAOnwGfKWkVgjdDq2wHsSKqkLA6AmVWBw3AsKgnf/0Pc2VtzIPPLKAfIAXKAHKCnADJ5oYQvo3v3XTSzC/wWKk3rBxbcuN6IhlqsYeCO37VXSfwWGGxpywHMbBy/N5xxxGmaB1wDe5KeGpr54zRrgB/90FZRdCs7PAAAAABJRU5ErkJggg=='


class FileBrowserPane:
    """Encapsulates an icon-based file system browser pane supporting local and UNC network paths."""

    def __init__(self, parent, title):
        self.current_path = os.path.abspath(os.getcwd())

        # 1. Create the container frame first
        self.frame = ttk.LabelFrame(parent, text=title)

        # --- Drive Selection Header Frame ---
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill="x", padx=5, pady=2)

        drives = []
        for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if os.path.exists(f"{d}:\\"):
                drives.append(f"{d}:\\")

        self.drive_var = tk.StringVar(value=self.current_path[:3] if len(self.current_path) >= 3 and self.current_path[1:3] == ":\\" else "")
        self.drive_combo = ttk.Combobox(
            top_frame,
            textvariable=self.drive_var,
            values=drives,
            state="readonly",
            width=6
        )
        self.drive_combo.pack(side="left", padx=(0, 5))
        self.drive_combo.bind("<<ComboboxSelected>>", self.change_drive)

        # --- Network Path Entry & Go Button ---
        self.unc_entry = Entry(top_frame, font=("Arial", 9))
        self.unc_entry.pack(side="left", fill="x", expand=True, padx=(0, 2))
        self.unc_entry.insert(0, "\\\\server\\share")
        self.unc_entry.bind("<Return>", lambda e: self.go_to_unc())

        go_btn = Button(top_frame, text="Go", command=self.go_to_unc, width=4)
        go_btn.pack(side="right")

        # 2. Path Display Label
        self.path_label = Label(
            self.frame,
            text=self.current_path,
            anchor="w",
            bg="white",
            relief="sunken",
            wraplength=280,
            justify="left"
        )
        self.path_label.pack(fill="x", padx=5, pady=2)

        # 3. Canvas and Scrollbar setup
        canvas_container = ttk.Frame(self.frame)
        canvas_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(canvas_container, bg="white", width=300, height=330)
        self.v_scrollbar = ttk.Scrollbar(
            canvas_container, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")

        self.content_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # 4. Cache PhotoImage instances
        self.file_icon = tk.PhotoImage(data=img)
        self.folder_icon = tk.PhotoImage(data=folder)

        self.dirlist = []

        # 5. Populate initial directory
        self.browsedir(self.current_path)

    def change_drive(self, event=None):
        new_drive = self.drive_var.get()
        if new_drive:
            self.browsedir(new_drive)

    def go_to_unc(self):
        target = self.unc_entry.get().strip()
        if target:
            self.browsedir(target)

    def browsedir(self, target_dir):
        """Populates the canvas with file/folder icons for target_dir without using os.chdir."""
        target_dir = os.path.normpath(target_dir)

        if not os.path.exists(target_dir):
            messagebox.showerror("Error", f"Path does not exist or is inaccessible:\n{target_dir}")
            return

        try:
            entries = os.listdir(target_dir)
        except PermissionError:
            messagebox.showerror("Error", "Permission Denied!")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Could not access path:\n{e}")
            return

        self.current_path = target_dir
        self.path_label.configure(text=self.current_path)

        # Update drive dropdown selection if navigating a local drive
        if len(self.current_path) >= 2 and self.current_path[1] == ":":
            self.drive_var.set(self.current_path[:3])
        else:
            self.drive_var.set("")

        # Clear existing items safely
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Separate items and sort
        dirs = []
        files = []
        for item in entries:
            full_item_path = os.path.join(self.current_path, item)
            try:
                if os.path.isdir(full_item_path):
                    dirs.append(item)
                else:
                    files.append(item)
            except OSError:
                files.append(item)

        dirs.sort(key=lambda s: s.lower())
        files.sort(key=lambda s: s.lower())

        self.dirlist = dirs + files

        # Add parent directory ".." option if not at the root level
        parent = os.path.dirname(self.current_path)
        if parent and parent != self.current_path:
            self.dirlist.insert(0, "..")

        style = ttk.Style()
        style.configure("Custom.TFrame", background="white")
        self.content_frame.configure(style="Custom.TFrame")

        x, y = 0, 0
        for item in self.dirlist:
            if item == "..":
                item_path = os.path.dirname(self.current_path)
                is_directory = True
            else:
                item_path = os.path.join(self.current_path, item)
                is_directory = item in dirs

            icon = self.folder_icon if is_directory else self.file_icon

            iconlabel = Label(self.content_frame, image=icon, bg="white")
            captionlabel = Label(
                self.content_frame,
                text=item,
                wraplength=60,
                bg="white",
                font=("Arial", 8),
            )

            iconlabel.grid(row=y, column=x, padx=2, pady=2)
            captionlabel.grid(row=y + 1, column=x, padx=2, pady=2)

            # Bind double click event
            iconlabel.bind("<Double-1>", lambda e, p=item_path: self.on_item_click(p))
            captionlabel.bind("<Double-1>", lambda e, p=item_path: self.on_item_click(p))

            x += 1
            if x > 3:
                x = 0
                y += 2

        self.content_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_item_click(self, target_path):
        if os.path.isdir(target_path):
            self.browsedir(target_path)


class RoboGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("RoboGUI")
        self.root.geometry("700x520")
        self.root.resizable(False, False)

        # Set App Icon

        faviconimg=b'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'

        self.favicon = tk.PhotoImage(data=faviconimg)
        self.root.wm_iconphoto(True, self.favicon)

        # Create Left (Source) and Right (Destination) Panes
        self.left_pane = FileBrowserPane(self.root, "Source Directory")
        self.left_pane.frame.place(x=10, y=10, width=335, height=440)

        self.right_pane = FileBrowserPane(self.root, "Destination Directory")
        self.right_pane.frame.place(x=355, y=10, width=335, height=440)

        # Control Buttons
        self.robo_button = Button(
            self.root, text="Robocopy", command=self.run_robocopy, bg="#e1e1e1"
        )
        self.robo_button.place(x=250, y=465, height=35, width=90)

        self.quit_button = Button(
            self.root, text="Exit", command=self.quit_program, bg="#e1e1e1"
        )
        self.quit_button.place(x=360, y=465, height=35, width=90)

    def run_robocopy(self):
        leftpath = self.left_pane.current_path
        rightpath = self.right_pane.current_path

        if leftpath == rightpath:
            messagebox.showwarning(
                "Warning", "Source and Destination directories are identical!"
            )
            return

        okcancel = messagebox.askokcancel(
            "Copy?",
            f"Do you want to copy:\n\nSource: {leftpath}\nDestination: {rightpath}?",
            default="ok",
        )
        if okcancel:
            command = f'start cmd /k robocopy "{leftpath}" "{rightpath}" /S /R:0 /W:0'
            os.system(command)

    def quit_program(self):
        okcancel = messagebox.askokcancel(
            "Exit?", "Do you want to exit the program?", default="ok"
        )
        if okcancel:
            self.root.destroy()


def main():
    root = tk.Tk()
    app = RoboGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

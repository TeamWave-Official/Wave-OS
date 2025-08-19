import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog

# Initialize window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Beautiful Bash Terminal")
app.geometry("800x500")

current_dir = os.getcwd()

# --- Output box ---
output_box = ctk.CTkTextbox(app, wrap="word", font=("Consolas", 14))
output_box.pack(fill="both", expand=True, padx=10, pady=10)
output_box.insert("end", f"{current_dir}$ ")

# --- Functions ---
def run_command(event=None):
    global current_dir
    command = input_box.get()
    input_box.delete(0, "end")

    if command.strip() == "":
        output_box.insert("end", f"\n{current_dir}$ ")
        return

    output_box.insert("end", command + "\n")

    parts = command.split()
    cmd = parts[0]

    try:
        if cmd == "cd":
            if len(parts) > 1:
                new_dir = os.path.abspath(os.path.join(current_dir, parts[1]))
                if os.path.isdir(new_dir):
                    current_dir = new_dir
                else:
                    output_box.insert("end", "No such directory\n")

        elif cmd == "ls" or cmd == "dir":
            files = os.listdir(current_dir)
            output_box.insert("end", "  ".join(files) + "\n")

        elif cmd == "mkdir":
            if len(parts) > 1:
                os.mkdir(os.path.join(current_dir, parts[1]))
            else:
                output_box.insert("end", "mkdir: missing operand\n")

        elif cmd == "touch":
            if len(parts) > 1:
                open(os.path.join(current_dir, parts[1]), 'a').close()
            else:
                output_box.insert("end", "touch: missing file\n")

        elif cmd.startswith("./"):
            file = cmd[2:]
            file_path = os.path.join(current_dir, file)
            if file.endswith(".py") and os.path.exists(file_path):
                result = subprocess.run(
                    ["python", file_path],
                    cwd=current_dir,
                    text=True,
                    capture_output=True
                )
                output_box.insert("end", result.stdout + result.stderr)
            else:
                output_box.insert("end", f"bash: {file}: command not found\n")

        elif cmd == "vim":
            if len(parts) > 1:
                filename = os.path.join(current_dir, parts[1])
                open_vim(filename)
            else:
                output_box.insert("end", "vim: missing file\n")

        elif cmd == "pkg":
            if len(parts) > 1 and parts[1] == "install":
                if len(parts) > 2 and parts[2] == "vim":
                    output_box.insert("end", "vim installed successfully (fake)\n")
                else:
                    output_box.insert("end", "package not found\n")
            else:
                output_box.insert("end", "Usage: pkg install <package>\n")

        else:
            output_box.insert("end", f"bash: {cmd}: command not found\n")

    except Exception as e:
        output_box.insert("end", f"Error: {str(e)}\n")

    output_box.insert("end", f"{current_dir}$ ")
    output_box.see("end")


def open_vim(filepath):
    vim = ctk.CTkToplevel(app)
    vim.title(f"VIM - {os.path.basename(filepath)}")
    vim.geometry("600x400")

    text_area = ctk.CTkTextbox(vim, font=("Consolas", 14))
    text_area.pack(fill="both", expand=True)

    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            text_area.insert("end", f.read())

    def save_file():
        with open(filepath, "w") as f:
            f.write(text_area.get("1.0", "end"))
        vim.destroy()

    save_btn = ctk.CTkButton(vim, text="Save & Exit", command=save_file)
    save_btn.pack(pady=5)

# --- Input box ---
input_box = ctk.CTkEntry(app, font=("Consolas", 14))
input_box.pack(fill="x", padx=10, pady=5)
input_box.bind("<Return>", run_command)

app.mainloop()

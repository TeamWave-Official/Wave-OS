import os
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

current_dir = os.getcwd()

def run_command(event=None):
    global current_dir
    command = entry.get().strip()
    if not command:
        return

    terminal_text.configure(state="normal")
    terminal_text.insert(ctk.END, f"$ {command}\n")

    parts = command.split()
    cmd = parts[0]
    args = parts[1:]

    if cmd == "clear":
        terminal_text.delete("1.0", ctk.END)
    elif cmd == "ls" or cmd == "dir":
        try:
            files = os.listdir(current_dir)
            terminal_text.insert(ctk.END, "\n".join(files) + "\n")
        except PermissionError:
            terminal_text.insert(ctk.END, "Permission denied\n")
    elif cmd == "cd":
        if not args:
            terminal_text.insert(ctk.END, "cd: missing argument\n")
        else:
            path = os.path.join(current_dir, args[0])
            if os.path.isdir(path):
                current_dir = os.path.abspath(path)
            else:
                terminal_text.insert(ctk.END, f"cd: no such directory: {args[0]}\n")
    elif cmd == "mkdir":
        if not args:
            terminal_text.insert(ctk.END, "mkdir: missing argument\n")
        else:
            try:
                os.mkdir(os.path.join(current_dir, args[0]))
            except FileExistsError:
                terminal_text.insert(ctk.END, f"mkdir: directory exists: {args[0]}\n")
    elif cmd == "touch":
        if not args:
            terminal_text.insert(ctk.END, "touch: missing argument\n")
        else:
            open(os.path.join(current_dir, args[0]), "a").close()
    else:
        terminal_text.insert(ctk.END, f"Command not found: {cmd}\n")

    terminal_text.see(ctk.END)
    terminal_text.configure(state="disabled")
    entry.delete(0, ctk.END)

root = ctk.CTk()
root.title("Python Bash Terminal")
root.geometry("700x500")

terminal_text = ctk.CTkTextbox(root, width=700, height=450)
terminal_text.pack(pady=10)
terminal_text.insert(ctk.END, f"Python Terminal - Current Dir: {current_dir}\n")
terminal_text.configure(state="disabled")  # make readonly

entry = ctk.CTkEntry(root, width=700)
entry.pack(pady=5)
entry.bind("<Return>", run_command)

root.mainloop()


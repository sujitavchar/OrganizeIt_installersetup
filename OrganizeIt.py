import os, shutil, threading, sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  #When bundled by PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


animation_texts = [
    "Categorizing 📄 Documents...",
    "Categorizing 🖼️ Images...",
    "Categorizing 🎵 Audio...",
    "Categorizing 🎞️ Videos...",
    "Categorizing 📦 Archives...",
    "Placing 🔄 Others..."
]

# Default rules 
DEFAULT_RULES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".txt", ".pdf", ".docx", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Archives": [".zip", ".tar", ".rar", ".gz"],
    "Others": []
}

def organize_files(directory, status_label, rules_text):
    status_label.config(text="🔄 Working...")

    try:
        # Load rules from the textbox
        rules_input = rules_text.get("1.0", tk.END)
        categories = json.loads(rules_input)
    except Exception as e:
        messagebox.showerror("Invalid Rules", f"Error in rules: {e}")
        status_label.config(text="❌ Invalid Rules")
        return

    # Create folders
    for category in categories:
        os.makedirs(os.path.join(directory, category), exist_ok=True)

    # Organize files
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path): continue
        _, ext = os.path.splitext(filename)
        moved = False
        for cat, exts in categories.items():
            if ext.lower() in exts:
                shutil.move(file_path, os.path.join(directory, cat, filename))
                moved = True
                break
        if not moved:
            shutil.move(file_path, os.path.join(directory, "Others", filename))

    status_label.config(text="✅ Organized Successfully!")
    messagebox.showinfo("Done", "Files have been organized.")

def start_organize(status_label, animation_label, rules_text):
    directory = filedialog.askdirectory(title="Select Folder")
    if not directory:
        messagebox.showwarning("No Folder", "No directory selected!")
        return

    threading.Thread(target=organize_files, args=(directory, status_label, rules_text)).start()

    def animate(i=0):
        if i < len(animation_texts):
            animation_label.config(text=animation_texts[i])
            animation_label.after(600, lambda: animate(i+1))
        else:
            animation_label.config(text="")

    animate()

def main():
    root = tk.Tk()
    root.title("🧠 OrganizeIt v2.0")
    root.state("zoomed")
    root.configure(bg="black")

    bg_label = tk.Label(root, bg="black")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    try:
        bg_path = resource_path("background.jpg")

        original_bg = Image.open(bg_path)

        def resize_bg(event):
            resized = original_bg.resize((event.width, event.height), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(resized)
            bg_label.config(image=bg_photo)
            bg_label.image = bg_photo

        root.bind("<Configure>", resize_bg)
    except Exception as e:
        print("Background image could not be loaded:", e)

    title = tk.Label(root, text="📁 OrganizeIt", font=("Segoe UI", 40, "bold"), fg="#ff6b00", bg="black")
    title.place(x=30, y=20)

    subtitle1 = tk.Label(root, text="Organize your messy folder in a single click...", font=("Segoe UI", 13), fg="white", bg="black")
    subtitle1.place(x=30, y=90)

    subtitle2 = tk.Label(root, text="Select the desired folder and let the magic happen.", font=("Segoe UI", 13), fg="white", bg="black")
    subtitle2.place(x=30, y=130)

    animation_label = tk.Label(root, text="", font=("Segoe UI", 12, "italic"), fg="#dddddd", bg="black")
    animation_label.place(x=30, y=160)

    status_label = tk.Label(root, text="", font=("Segoe UI", 11), fg="#55ff55", bg="black")
    status_label.place(x=30, y=200)

    # RULES TEXTBOX
    rules_label = tk.Label(root, text="✏️ Edit File Type Rules (JSON):", font=("Segoe UI", 11), fg="white", bg="black")
    rules_label.place(x=30, y=250)

    rules_text = tk.Text(root, height=10, width=80, font=("Consolas", 10))
    rules_text.place(x=30, y=280)
    rules_text.insert(tk.END, json.dumps(DEFAULT_RULES, indent=4))

    action_btn = tk.Button(
        root,
        text="📂 Select Folder & Organize",
        command=lambda: start_organize(status_label, animation_label, rules_text),
        font=("Segoe UI", 13, "bold"),
        bg="#4B0082",
        fg="white",
        activebackground="#36005d",
        activeforeground="white",
        relief="flat",
        padx=20,
        pady=10
    )
    action_btn.place(relx=0.5, y=470, anchor="center")

    footer = tk.Label(root, text="Designed & Developed by Sujit Avchar", font=("Segoe UI", 9), fg="#aaaaaa", bg="black")
    footer.place(relx=0.5, rely=1.0, y=-20, anchor="s")

    root.mainloop()

if __name__ == "__main__":
    main()

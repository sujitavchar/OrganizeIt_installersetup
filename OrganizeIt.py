import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def organize_files(directory):
    # If the directory doesn't exist, return
    if not os.path.exists(directory):
        messagebox.showerror("Error", f"The directory {directory} does not exist.")
        return

    # Define categories (file types)
    categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
        'Documents': ['.txt', '.pdf', '.docx', '.xlsx', '.pptx'],
        'Audio': ['.mp3', '.wav', '.aac', '.flac'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov'],
        'Archives': ['.zip', '.tar', '.rar', '.gz'],
        'Others': []
    }

    # Create folders for each category if not already present
    for category in categories.keys():
        category_folder = os.path.join(directory, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

    # Organize files
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Skip if it's a folder
        if os.path.isdir(file_path):
            continue
        
        # Get the file extension
        _, file_extension = os.path.splitext(filename)
        
        # Determine which category the file belongs to
        categorized = False
        for category, extensions in categories.items():
            if file_extension.lower() in extensions:
                category_folder = os.path.join(directory, category)
                shutil.move(file_path, os.path.join(category_folder, filename))
                categorized = True
                print(f"Moved {filename} to {category} folder.")
                break
        
        # If no category is found, move it to 'Others'
        if not categorized:
            category_folder = os.path.join(directory, 'Others')
            shutil.move(file_path, os.path.join(category_folder, filename))
            print(f"Moved {filename} to Others folder.")
    
    messagebox.showinfo("Success", "Files have been organized successfully.")

def select_directory():
    # Create a file dialog to select the directory
    directory = filedialog.askdirectory(title="Select a Directory")
    if directory:
        organize_files(directory)
    else:
        messagebox.showwarning("No Directory Selected", "Please select a directory to organize.")

def main():
    # Create a tkinter GUI
    root = tk.Tk()
    root.title("Organize Files")
    root.geometry("300x150")
    root.tk.call("tk", "scaling", 1.5)

    label = tk.Label(root, text="Click the button to select a folder:", font=("Roboto", 12))
    label.pack(pady=20)

    button = tk.Button(root, text="Select Folder", command=select_directory, font=("Roboto", 12))
    button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

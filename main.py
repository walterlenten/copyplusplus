import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

class FileCopyApp:
    def __init__(self, master):
        self.master = master
        master.title("File Copy Utility")
        
        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        
        # Source selection
        tk.Label(master, text="Source File:").grid(row=0, column=0, sticky="e")
        tk.Entry(master, textvariable=self.source_path, width=50).grid(row=0, column=1)
        tk.Button(master, text="Browse", command=self.browse_source).grid(row=0, column=2)
        
        # Destination selection
        tk.Label(master, text="Destination Folder:").grid(row=1, column=0, sticky="e")
        tk.Entry(master, textvariable=self.dest_path, width=50).grid(row=1, column=1)
        tk.Button(master, text="Browse", command=self.browse_destination).grid(row=1, column=2)
        
        # Copy button
        tk.Button(master, text="Copy File", command=self.copy_file).grid(row=2, column=1)

    def browse_source(self):
        filename = filedialog.askopenfilename(initialdir="/Volumes")
        self.source_path.set(filename)

    def browse_destination(self):
        dirname = filedialog.askdirectory(initialdir="/Volumes")
        self.dest_path.set(dirname)

    def copy_file(self):
        source = self.source_path.get()
        destination = self.dest_path.get()
        
        if not source or not destination:
            messagebox.showerror("Error", "Please select both source and destination.")
            return
        
        try:
            shutil.copy2(source, destination)
            messagebox.showinfo("Success", f"File copied successfully to {destination}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCopyApp(root)
    root.mainloop()
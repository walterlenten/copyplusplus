import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import time
import threading

class FileCopyApp:
    def __init__(self, master):
        self.master = master
        master.title("File Copy Utility")
        master.geometry("550x400")  # Initial size, but now resizable
        
        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        
        # Configure root window grid
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)
        
        # Main frame
        main_frame = tk.Frame(master)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Source selection
        tk.Label(main_frame, text="Source File:").grid(row=0, column=0, sticky="e", pady=5)
        tk.Entry(main_frame, textvariable=self.source_path).grid(row=0, column=1, sticky="ew", pady=5)
        tk.Button(main_frame, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)
        
        # Destination selection
        tk.Label(main_frame, text="Destination Folder:").grid(row=1, column=0, sticky="e", pady=5)
        tk.Entry(main_frame, textvariable=self.dest_path).grid(row=1, column=1, sticky="ew", pady=5)
        tk.Button(main_frame, text="Browse", command=self.browse_destination).grid(row=1, column=2, padx=5, pady=5)
        
        # Copy button
        self.copy_button = tk.Button(main_frame, text="Copy File", command=self.start_copy)
        self.copy_button.grid(row=2, column=1, pady=10)
        
        # Progress frame
        progress_frame = tk.Frame(master)
        progress_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        progress_frame.grid_columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
        self.progress.grid(row=0, column=0, sticky="ew", pady=5)
        
        # Status labels
        self.time_label = tk.Label(progress_frame, text="Estimated time remaining: ")
        self.time_label.grid(row=1, column=0, sticky="w", pady=2)
        
        self.size_label = tk.Label(progress_frame, text="Remaining file size: ")
        self.size_label.grid(row=2, column=0, sticky="w", pady=2)

        # Initially hide progress bar and labels
        self.progress.grid_remove()
        self.time_label.grid_remove()
        self.size_label.grid_remove()

    def browse_source(self):
        filename = filedialog.askopenfilename(initialdir="/Volumes")
        self.source_path.set(filename)

    def browse_destination(self):
        dirname = filedialog.askdirectory(initialdir="/Volumes")
        self.dest_path.set(dirname)

    def start_copy(self):
        source = self.source_path.get()
        destination = self.dest_path.get()
        
        if not source or not destination:
            messagebox.showerror("Error", "Please select both source and destination.")
            return
        
        # Show progress elements
        self.show_progress_elements()
        
        # Start copying in a separate thread
        threading.Thread(target=self.copy_file, args=(source, destination)).start()

    def show_progress_elements(self):
        self.copy_button.config(state=tk.DISABLED)
        self.progress.grid()
        self.time_label.grid()
        self.size_label.grid()
        
        # Slide-down animation
        for widget in [self.progress, self.time_label, self.size_label]:
            widget.grid_remove()
            widget.grid()
            for i in range(11):
                widget.grid(pady=(i*2, 0))
                self.master.update_idletasks()
                time.sleep(0.01)

    def hide_progress_elements(self):
        self.copy_button.config(state=tk.NORMAL)
        # Slide-up animation
        for widget in [self.size_label, self.time_label, self.progress]:
            for i in range(10, -1, -1):
                widget.grid(pady=(i*2, 0))
                self.master.update_idletasks()
                time.sleep(0.01)
            widget.grid_remove()

    def copy_file(self, source, destination):
        try:
            file_size = os.path.getsize(source)
            basename = os.path.basename(source)
            dest_path = os.path.join(destination, basename)
            
            with open(source, 'rb') as src, open(dest_path, 'wb') as dst:
                copied = 0
                start_time = time.time()
                
                while True:
                    buf = src.read(4096)  # Read in 4KB chunks
                    if not buf:
                        break
                    dst.write(buf)
                    copied += len(buf)
                    
                    # Update progress
                    progress = (copied / file_size) * 100
                    self.progress['value'] = progress
                    
                    # Update time and size remaining
                    elapsed_time = time.time() - start_time
                    speed = copied / elapsed_time if elapsed_time > 0 else 0
                    remaining_size = file_size - copied
                    remaining_time = remaining_size / speed if speed > 0 else 0
                    
                    self.master.after(0, self.update_labels, remaining_time, remaining_size)
                    
                    self.master.update_idletasks()

            messagebox.showinfo("Success", f"File copied successfully to {destination}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.progress['value'] = 0
            self.time_label.config(text="Estimated time remaining: ")
            self.size_label.config(text="Remaining file size: ")
            self.master.after(0, self.hide_progress_elements)

    def update_labels(self, remaining_time, remaining_size):
        self.time_label.config(text=f"Estimated time remaining: {remaining_time:.2f} seconds")
        self.size_label.config(text=f"Remaining file size: {self.format_size(remaining_size)}")

    @staticmethod
    def format_size(size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCopyApp(root)
    root.mainloop()
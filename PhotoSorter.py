import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import mimetypes
from tkinter.font import Font
import sv_ttk 

class ModernPhotoOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Organizer")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        sv_ttk.set_theme("light")
        
        # Custom fonts
        self.header_font = Font(family="Segoe UI", size=16, weight="bold")
        self.regular_font = Font(family="Segoe UI", size=10)
        
        # Create main container with padding
        self.main_container = ttk.Frame(root, padding="20")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Header
        header_frame = ttk.Frame(self.main_container)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        ttk.Label(header_frame, text="Photo Organizer", font=self.header_font).pack(side=tk.LEFT)
        
        # Create content frame
        content_frame = ttk.Frame(self.main_container)
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(1, weight=1)
        
        # Folder selection section
        self.create_folder_selection_section(content_frame)
        
        # Sorting options section
        self.create_sorting_section(content_frame)
        
        # Progress section
        self.create_progress_section(content_frame)
        
        # Action buttons section
        self.create_action_section(content_frame)
        
        # Status bar at the bottom
        self.create_status_bar()

    def create_folder_selection_section(self, parent):
        folder_frame = ttk.LabelFrame(parent, text="Folder Selection", padding="10")
        folder_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Source folder
        ttk.Label(folder_frame, text="Source:", font=self.regular_font).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.source_var = tk.StringVar()
        source_entry = ttk.Entry(folder_frame, textvariable=self.source_var, width=50)
        source_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(folder_frame, text="Browse", command=self.browse_source, style='Accent.TButton').grid(row=0, column=2, padx=5)
        
        # Destination folder
        ttk.Label(folder_frame, text="Destination:", font=self.regular_font).grid(row=1, column=0, sticky=tk.W, padx=5, pady=10)
        self.dest_var = tk.StringVar()
        dest_entry = ttk.Entry(folder_frame, textvariable=self.dest_var, width=50)
        dest_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=10)
        ttk.Button(folder_frame, text="Browse", command=self.browse_dest, style='Accent.TButton').grid(row=1, column=2, padx=5, pady=10)

    def create_sorting_section(self, parent):
        sort_frame = ttk.LabelFrame(parent, text="Organization Settings", padding="10")
        sort_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Sorting method
        ttk.Label(sort_frame, text="Sort files by:", font=self.regular_font).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.sort_method = tk.StringVar(value="date")
        sort_combo = ttk.Combobox(sort_frame, textvariable=self.sort_method, width=30, state='readonly')
        sort_combo['values'] = ('Date (Year/Month)', 'File Type (Image, Video, etc.)', 'File Size (Small, Medium, Large)')
        sort_combo.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Add sorting method descriptions
        descriptions = {
            'Date': 'Organizes files into Year/Month folders based on creation date',
            'File Type': 'Groups files by their type (images, videos, documents, etc.)',
            'File Size': 'Categorizes files into Small (<1MB), Medium (1-10MB), and Large (>10MB)'
        }
        
        desc_frame = ttk.Frame(sort_frame)
        desc_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        self.desc_label = ttk.Label(desc_frame, text=descriptions['Date'], font=self.regular_font, wraplength=500)
        self.desc_label.pack(anchor=tk.W)
        
        def update_description(event):
            selected = sort_combo.get()
            if 'Date' in selected:
                self.desc_label.config(text=descriptions['Date'])
            elif 'File Type' in selected:
                self.desc_label.config(text=descriptions['File Type'])
            elif 'File Size' in selected:
                self.desc_label.config(text=descriptions['File Size'])
        
        sort_combo.bind('<<ComboboxSelected>>', update_description)

    def create_progress_section(self, parent):
        progress_frame = ttk.LabelFrame(parent, text="Progress", padding="10")
        progress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, mode='determinate', length=400)
        self.progress.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Progress labels
        self.progress_label = ttk.Label(progress_frame, text="Ready to organize", font=self.regular_font)
        self.progress_label.grid(row=1, column=0, sticky=tk.W, padx=5)
        
        self.file_count_label = ttk.Label(progress_frame, text="Files: 0/0", font=self.regular_font)
        self.file_count_label.grid(row=1, column=1, sticky=tk.E, padx=5)

    def create_action_section(self, parent):
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Organize button
        self.organize_btn = ttk.Button(
            action_frame,
            text="Organize Photos",
            command=self.organize_photos,
            style='Accent.TButton',
            width=20
        )
        self.organize_btn.pack(pady=10)

    def create_status_bar(self):
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            font=self.regular_font,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(10, 5)
        )
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def browse_source(self):
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_var.set(folder)
            self.status_var.set(f"Source folder selected: {folder}")

    def browse_dest(self):
        folder = filedialog.askdirectory(title="Select Destination Folder")
        if folder:
            self.dest_var.set(folder)
            self.status_var.set(f"Destination folder selected: {folder}")

    def get_sort_method(self):
        selected = self.sort_method.get()
        if 'Date' in selected:
            return 'date'
        elif 'File Type' in selected:
            return 'file_type'
        else:
            return 'file_size'

    def get_file_category(self, file_path):
        file_size = os.path.getsize(file_path)
        if file_size < 1024 * 1024:  # Less than 1MB
            return "small_files"
        elif file_size < 10 * 1024 * 1024:  # Less than 10MB
            return "medium_files"
        else:
            return "large_files"

    def get_destination_path(self, file_path, filename):
        base_dest = self.dest_var.get()
        sort_method = self.get_sort_method()

        if sort_method == "date":
            creation_time = os.path.getctime(file_path)
            date_time = datetime.utcfromtimestamp(creation_time)
            return os.path.join(base_dest, str(date_time.year), str(date_time.month))
        
        elif sort_method == "file_type":
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                file_type = "other"
            else:
                file_type = mime_type.split('/')[0]
            return os.path.join(base_dest, file_type)
        
        elif sort_method == "file_size":
            size_category = self.get_file_category(file_path)
            return os.path.join(base_dest, size_category)

    def organize_photos(self):
        source_folder = self.source_var.get()
        destination_folder = self.dest_var.get()
        
        if not source_folder or not destination_folder:
            messagebox.showerror("Error", "Please select both source and destination folders")
            return
        
        try:
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            
            files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
            total_files = len(files)
            processed_files = 0
            
            self.organize_btn.state(['disabled'])
            self.progress_var.set(0)
            self.progress_label.config(text="Organizing files...")
            
            for filename in files:
                file_path = os.path.join(source_folder, filename)
                
                try:
                    dest_folder = self.get_destination_path(file_path, filename)
                    
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                    
                    shutil.move(file_path, os.path.join(dest_folder, filename))
                    
                    processed_files += 1
                    progress = (processed_files / total_files) * 100
                    self.progress_var.set(progress)
                    self.progress_label.config(text=f"Processing: {filename}")
                    self.file_count_label.config(text=f"Files: {processed_files}/{total_files}")
                    self.status_var.set(f"Organizing: {processed_files}/{total_files} files completed")
                    self.root.update()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error processing {filename}: {e}")
            
            self.progress_label.config(text="Organization complete!")
            self.status_var.set("Organization complete!")
            messagebox.showinfo("Success", "Files have been organized successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        
        finally:
            self.organize_btn.state(['!disabled'])
            self.progress_label.config(text="Ready to organize")
            self.file_count_label.config(text="Files: 0/0")

def main():
    root = tk.Tk()
    root.title("Photo Organizer")
    
    # Set window icon (if you have one)
    # root.iconbitmap('path_to_icon.ico')
    
    # Set minimum window size
    root.minsize(800, 600)
    
    app = ModernPhotoOrganizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

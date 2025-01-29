from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Function to resize the image
def resize_image():
    try:
        # Get user inputs
        width = int(width_entry.get())
        height = int(height_entry.get())
        image_path = file_path.get()

        if not image_path:
            messagebox.showerror("Error", "Please select an image file!")
            return

        # Open the image
        img = Image.open(image_path)
        # Resize the image
        resized_img = img.resize((width, height), Image.ANTIALIAS)
        # Save the resized image
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if save_path:
            resized_img.save(save_path)
            messagebox.showinfo("Success", f"Image resized and saved to {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to open and display the selected image
def open_image():
    file_path.set(filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]))
    if file_path.get():
        img = Image.open(file_path.get())
        img.thumbnail((200, 200))  # Resize for preview
        img = ImageTk.PhotoImage(img)
        preview_label.config(image=img)
        preview_label.image = img  # Keep a reference to avoid garbage collection

# Create the main window
root = Tk()
root.title("Image Resizer")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Modern styling
font = ("Arial", 10)
entry_bg = "#ffffff"
button_bg = "#4CAF50"
button_fg = "#ffffff"

# Variables
file_path = StringVar()

# GUI Elements
Label(root, text="Image Resizer", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

# File selection
file_frame = Frame(root, bg="#f0f0f0")
file_frame.pack(pady=5)
Label(file_frame, text="Select Image:", font=font, bg="#f0f0f0").pack(side=LEFT, padx=5)
Entry(file_frame, textvariable=file_path, width=30, font=font, bg=entry_bg, state="readonly").pack(side=LEFT, padx=5)
Button(file_frame, text="Browse", font=font, bg=button_bg, fg=button_fg, command=open_image).pack(side=LEFT, padx=5)

# Width and Height inputs
input_frame = Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)
Label(input_frame, text="Width:", font=font, bg="#f0f0f0").grid(row=0, column=0, padx=5)
width_entry = Entry(input_frame, font=font, bg=entry_bg, width=10)
width_entry.grid(row=0, column=1, padx=5)
Label(input_frame, text="Height:", font=font, bg="#f0f0f0").grid(row=0, column=2, padx=5)
height_entry = Entry(input_frame, font=font, bg=entry_bg, width=10)
height_entry.grid(row=0, column=3, padx=5)

# Preview image
preview_label = Label(root, bg="#f0f0f0")
preview_label.pack(pady=10)

# Resize button
Button(root, text="Resize Image", font=font, bg=button_bg, fg=button_fg, command=resize_image).pack(pady=10)

# Run the application
root.mainloop()

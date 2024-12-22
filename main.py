from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Initialize the main window
root = Tk()
root.title("Image Watermarking Tool")
root.geometry("600x500")
root.resizable(False, False)

# Global variables to hold image data
selected_image = None
image_display = None
watermarked_image = None


# Function to upload an image
def upload_image():
    global selected_image, image_display

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if file_path:
        selected_image = Image.open(file_path)
        selected_image.thumbnail((300, 300))

        image_display = ImageTk.PhotoImage(selected_image)
        image_label.config(image=image_display)
        image_label.image = image_display
        messagebox.showinfo("Image Upload", "Image uploaded successfully!")


# Function to add watermark
def add_watermark():
    global selected_image, watermarked_image

    if not selected_image:
        messagebox.showerror("Error", "Please upload an image first!")
        return

    watermark_text = watermark_entry.get()
    if not watermark_text:
        messagebox.showerror("Error", "Please enter watermark text!")
        return

    watermarked_image = selected_image.copy()
    draw = ImageDraw.Draw(watermarked_image)

    # Set font and size for watermark
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    # Calculate text size using textbbox()
    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Add watermark at bottom-right corner
    position = (watermarked_image.width - text_width - 10, watermarked_image.height - text_height - 10)
    draw.text(position, watermark_text, fill=(255, 255, 255, 128), font=font)

    watermarked_display = ImageTk.PhotoImage(watermarked_image)
    image_label.config(image=watermarked_display)
    image_label.image = watermarked_display

    messagebox.showinfo("Watermark", "Watermark added successfully!")


# Function to save the watermarked image
def save_image():
    global watermarked_image

    if not watermarked_image:
        messagebox.showerror("Error", "No watermarked image to save!")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
    )
    if file_path:
        watermarked_image.save(file_path)
        messagebox.showinfo("Save Image", "Watermarked image saved successfully!")


# GUI Layout
# Title Label
ttk.Label(root, text="Image Watermarking Tool", font=("Arial", 18)).pack(pady=10)

# Image Display Area (with Preloaded Image)
try:
    selected_image = Image.open("saumil_photo.jpg")
    selected_image.thumbnail((300, 300))
    image_display = ImageTk.PhotoImage(selected_image)
except FileNotFoundError:
    image_display = None
    print("Error: 'saumil_photo.jpg' not found. Please ensure the file exists in the working directory.")

# Image Label (to display the image)
image_label = Label(root, text="No Image Uploaded", width=50, height=15, bg="gray")
image_label.pack(pady=10)

if image_display:
    image_label.config(image=image_display)
    image_label.image = image_display

# Watermark Text Entry
ttk.Label(root, text="Enter Watermark Text:").pack(pady=5)
watermark_entry = ttk.Entry(root, width=30)
watermark_entry.pack(pady=5)

# Buttons
button_frame = Frame(root)
button_frame.pack(pady=10)

upload_btn = ttk.Button(button_frame, text="Upload Image", command=upload_image)
upload_btn.grid(row=0, column=0, padx=5)

watermark_btn = ttk.Button(button_frame, text="Add Watermark", command=add_watermark)
watermark_btn.grid(row=0, column=1, padx=5)

save_btn = ttk.Button(button_frame, text="Save Image", command=save_image)
save_btn.grid(row=0, column=2, padx=5)

quit_btn = ttk.Button(root, text="Quit", command=root.destroy)
quit_btn.pack(pady=10)

# Run the application
root.mainloop()

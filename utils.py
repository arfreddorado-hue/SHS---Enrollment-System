import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

def display_background(root):
    image_path = r"C:/Users/User/Downloads/mainwindow.png"
    bg_image = Image.open(image_path)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_color = '#273b7a'

    root.bg_photo = bg_photo

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

def make_layout(root):
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry(f"{w}x{h}+0+0")

def make_icon(path, size=(60, 60)):
    img = Image.open(path).resize(size, Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", size, 1)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    img.putalpha(mask)
    return ImageTk.PhotoImage(img)

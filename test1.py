from PIL import Image, ImageTk
import numpy as np
import io as io1
from skimage.morphology import skeletonize
from skimage.util import invert
from skimage import io
from skimage.color import rgb2gray
import tkinter as tk

frames = []
skeleframes = []

def gif_to_array(gif_path):
    global frames
    
    gif = Image.open(gif_path)
    frames.clear()

    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgb = gif.convert('RGB')
        jpeg_io = io1.BytesIO()
        frame_rgb.save(jpeg_io, format='JPEG')
        jpeg_io.seek(0)
        frame_jpeg = Image.open(jpeg_io)
        frame_array = np.array(frame_jpeg)
        frames.append(frame_array)

def convert_to_tk_image(image):
    image = Image.fromarray(image.astype(np.uint8) * 255)
    return ImageTk.PhotoImage(image)

gif_file = 'danceman.gif'
gif_to_array(gif_file)

for f in frames:
    image = f
    if image.ndim == 3:
        image_gray = rgb2gray(image)
    else:
        image_gray = image
    threshold = 0.5
    binary_image = image_gray > threshold
    # inverted_binary_image = invert(binary_image)
    inverted_binary_image = binary_image
    skeleframes.append(skeletonize(inverted_binary_image))

def show_image():
    root = tk.Tk()
    root.title("Giffy")

    img_label = tk.Label(root)
    img_label.pack()

    def changeimgonebyone():
        global inum
        if inum < len(frames):
            img = convert_to_tk_image(skeleframes[inum])
            img_label.config(image=img)
            img_label.image = img  # Keep a reference to avoid garbage collection
            inum += 1
        else:
            inum = 0

        root.after(70, changeimgonebyone)
    global inum
    inum = 0
    root.after(10, changeimgonebyone)
    root.mainloop()

show_image()

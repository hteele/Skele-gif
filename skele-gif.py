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

# Convert input gif to array
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

# Needed because the images are actually numpy arrays, so we need to change them
def convert_original_to_tk_image(image):
    image = Image.fromarray(image.astype(np.uint8))
    return ImageTk.PhotoImage(image)

# Needed because the images are actually numpy arrays, so we need to change them
def convert_new_to_tk_image(image):
    image = Image.fromarray(image.astype(np.uint8)*255)
    return ImageTk.PhotoImage(image)


gif_file = './gifs-pics/zingus-cat.gif'
gif_to_array(gif_file)

for f in frames:
    image = f
    if image.ndim == 3:
        image_gray = rgb2gray(image)
    else:
        image_gray = image
    threshold = 0.5

    # ---------- INVERSION CONDITION  -----------
    binary_image = image_gray > threshold
    if binary_image[0, 0] == 1:
        skeleframes.append(skeletonize(invert(binary_image)))
    else:
        skeleframes.append(skeletonize(binary_image))
    # --------- END OF INVERSION --------------

def show_images():
    root = tk.Tk()
    root.title("Skeleton Project")

    original_label = tk.Label(root)
    original_label.pack()

    skeleton_label = tk.Label(root)
    skeleton_label.pack()

    # Function that iterates over the gif frames to display as a label
    # Runs infinitely
    def changeimgonebyone():
        global inum
        if inum < len(frames):
            orig_img = convert_original_to_tk_image(frames[inum])
            original_label.config(image=orig_img)
            original_label.image = orig_img  # Keep a reference to avoid garbage collection

            skele_img = convert_new_to_tk_image(skeleframes[inum])
            skeleton_label.config(image=skele_img)
            skeleton_label.image = skele_img  # Keep a reference to avoid garbage collection
            inum += 1
        else:
            inum = 0

        root.after(70, changeimgonebyone) # Time delay term

    global inum
    inum = 0
    root.after(10, changeimgonebyone) # Time delay term
    root.mainloop()

show_images()
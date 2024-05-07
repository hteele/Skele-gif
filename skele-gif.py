from PIL import Image, ImageTk
import numpy as np
import io as io1
from skimage.morphology import skeletonize
from skimage.util import invert
from skimage import io
from skimage.color import rgb2gray
import tkinter as tk
from tkinter import filedialog

frames = []
skeleframes = []

# Convert input gif to array
def gif_to_array(gif_path):

    global frames
    gif = Image.open(gif_path)
    frames.clear()
    skeleframes.clear()

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

def setSkeleframes():
    for f in frames:
        image = f
        if image.ndim == 3:
            image_gray = rgb2gray(image)
        else:
            image_gray = image

        # ---------- INVERSION CONDITION  -----------
        threshold = 0.5
        binary_image = image_gray > threshold
        if binary_image[0, 0] == 1:
            skeleframes.append(skeletonize(invert(binary_image)))
        else:
            skeleframes.append(skeletonize(binary_image))
        # ------------ END OF INVERSION --------------

# Open File function
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if file_path:
        try:
            # Attempt to open the file using PIL
            img = Image.open(file_path)
            gif_to_array(file_path)
            setSkeleframes()
            print("Selected file:", file_path)
            # Proceed with the file
        except IOError:
            # If the file cannot be opened, show an error message
            print("Error: Not a valid GIF file")

# Recursive display loop with delays to update the output frames at the gif rate
def display():
    root = tk.Tk()
    root.title("Skeleton Project")
    root.resizable(False, False)

    # BEGIN EXPERIMENTAL FILE CODE
    button = tk.Button(root, text="Open GIF File", command=open_file, width=50, height=2)
    button.pack(side=tk.TOP)

    # BELOW IS THE WORKING GIF CODE
    original_label = tk.Label(root)
    original_label.pack(side=tk.LEFT)

    skeleton_label = tk.Label(root)
    skeleton_label.pack(side=tk.LEFT)

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

        root.after(70, changeimgonebyone)  # Time delay term -- Controls framerate of the GIF

    # Begin recursive loop
    global inum
    inum = 0
    root.after(0, changeimgonebyone)  # Time delay term is technically unnecessary, so 0
    root.mainloop()  # Call display window

display()
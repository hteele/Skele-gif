from PIL import Image
import numpy as np
import io as io1
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt
from skimage.util import invert
from skimage import io
from skimage.color import rgb2gray
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

frames = []
skeleframes = []

def gif_to_array(gif_path):
    global frames
    
    # Open the GIF file
    gif = Image.open(gif_path)
    
    # Clear frames array for each new GIF
    frames.clear()

    # Iterate over each frame
    for frame_index in range(gif.n_frames):
        # Go to the current frame
        gif.seek(frame_index)
        
        # Convert the frame to RGB mode
        frame_rgb = gif.convert('RGB')
        
        # Save the frame as JPEG in memory
        jpeg_io = io1.BytesIO()
        frame_rgb.save(jpeg_io, format='JPEG')
        
        # Load the JPEG image back
        jpeg_io.seek(0)
        frame_jpeg = Image.open(jpeg_io)
        
        # Convert the frame to numpy array
        frame_array = np.array(frame_jpeg)
        
        # Append the frame array to the global list of frames
        frames.append(frame_array)

# Example usage
# gif_file = 'catspingif.gif'
gif_file = 'zingus-cat.gif'
gif_to_array(gif_file)
# print(len(frames))  # Number of frames in the GIF

# Load your own image
# image_path = "horsebinary.jpg"
# image_path = frames[1]
image = frames[22] # io.imread(image_path)

# Convert the image to grayscale if it's not already
if image.ndim == 3:
    image_gray = rgb2gray(image)
else:
    image_gray = image

# Convert the grayscale image to binary by thresholding
threshold = 0.5  # Adjust threshold as needed
binary_image = image_gray > threshold

# Invert the binary image
# inverted_binary_image = binary_image
inverted_binary_image = invert(binary_image)

# Perform skeletonization
skeleton = skeletonize(inverted_binary_image)


for f in frames:
    image = f
    if image.ndim == 3:
        image_gray = rgb2gray(image)
    else:
        image_gray = image
    threshold = 0.5  # Adjust threshold as needed
    binary_image = image_gray > threshold
    inverted_binary_image = invert(binary_image)
    skeleframes.append(skeletonize(inverted_binary_image))

# Display results
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4), sharex=True, sharey=True)

# ax = axes.ravel()

# ax[0].imshow(inverted_binary_image, cmap=plt.cm.gray)
# ax[0].axis('off')
# ax[0].set_title('original', fontsize=20)

# ax[1].imshow(skeleton, cmap=plt.cm.gray)
# ax[1].axis('off')
# ax[1].set_title('skeleton', fontsize=20)

# fig.tight_layout()
# plt.show()

def convert_to_tk_image(image):
    image = Image.fromarray(image.astype(np.uint8) * 255)
    return ImageTk.PhotoImage(image)

def show_image():
    root = tk.Tk()
    root.title("Giffy")

    def changeimgonebyone():
        global inum
        if inum < len(frames):
            img = convert_to_tk_image(skeleframes[inum])
            # img =  ImageTk.PhotoImage(image=Image.fromarray(skeleframes))
            img_label.config(image=img)
            inum += 1
        else:
            inum = 0  # Reset counter when reaching the end

        root.after(70, changeimgonebyone)  # Schedule the next call after 1000 milliseconds

    # Load the initial images using the resource_path function
    

    # Create a label to display the image
    global img_label
    img_label = tk.Label(root, image=skeleframes[0])
    img_label.pack()

    # Initialize inum before calling the changeimgonebyone function
    global inum
    inum = 0

    # Schedule the initial call of the changeimgonebyone function
    root.after(10, changeimgonebyone)

    root.mainloop()

# Call the function to show the changing image
show_image()
import os
import numpy as np
from skimage.morphology import skeletonize
import matplotlib.pyplot as plt
from skimage.util import invert
from skimage import io
from skimage.color import rgb2gray

inputDir = 'NAME'
outputDir = 'NAME'

if not os.path.exists(outputDir):
    os.makedirs(outputDir)
    
file_list = [f for f in os.listdir(inputDir) if f.endswith('.png')]

for file_name in file_list:
    image_path = os.path.join(inputDir, file_name)
    image = io.imread(image_path)

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

    skeleton_file_name = 'SKELETON_' + file_name
    skeleton_file_path = os.path.join(outputDir, skeleton_file_name)
    io.imsave(skeleton_file_path, skeleton.astype(np.uint8)*255)
    
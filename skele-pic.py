from skimage.morphology import skeletonize
import matplotlib.pyplot as plt
from skimage.util import invert
from skimage import io
from skimage.color import rgb2gray

# Load your own image
# image_path = "horsebinary.jpg"
image_path = "catwhitebackground.png"
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

# Display results
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4), sharex=True, sharey=True)

ax = axes.ravel()

ax[0].imshow(inverted_binary_image, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('original', fontsize=20)

ax[1].imshow(skeleton, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('skeleton', fontsize=20)

fig.tight_layout()
plt.show()

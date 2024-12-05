import bayer
import matplotlib.pyplot as plt
import numpy as np

# Read the images
image_rgb = plt.imread('./1024px-Colouring_pencils.jpg')
image_rggb = plt.imread('./1024px-Colouring_pencils_RGGB.png')
image_grbg = plt.imread('./1024px-Colouring_pencils_GRBG.png')
image_gbrg = plt.imread('./1024px-Colouring_pencils_GBRG.png')
image_bggr = plt.imread('./1024px-Colouring_pencils_BGGR.png')

# Convert images to uint8 (if necessary)
image_rggb = np.uint8(image_rggb * 255)
image_grbg = np.uint8(image_grbg * 255)
image_gbrg = np.uint8(image_gbrg * 255)
image_bggr = np.uint8(image_bggr * 255)

# Create a figure to display the images
fig, axes = plt.subplots(1, 5, figsize=(15, 5))

# Display each image
axes[0].imshow(image_rgb)
axes[1].imshow(bayer.bayer_to_rgb(image_rggb, 'RGGB', True))
axes[2].imshow(bayer.bayer_to_rgb(image_grbg, 'GRBG', True))
axes[3].imshow(bayer.bayer_to_rgb(image_gbrg, 'GBRG', True))
axes[4].imshow(bayer.bayer_to_rgb(image_bggr, 'BGGR', True))

# Remove axis labels and ticks
for ax in axes:
    ax.axis('off')

# Show the plot
plt.show()
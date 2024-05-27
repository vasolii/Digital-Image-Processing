from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from my_img_rotation import my_img_rotation

#set the filepath to the image file
filename = "im2.jpg"

#read the image into a PIL entity
img = Image.open(filename)

#obtain the underlying np array
img_arr = np.array(img,dtype=np.uint8)

# Rotation angles in radians
angle_54_deg = 54 * np.pi / 180
angle_213_deg = 213 * np.pi / 180

# Create subplots
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# Plot original image
axs[0].imshow(img_arr)
axs[0].set_title('Original')

# Rotate by 54 degrees
rot_img_54 = my_img_rotation(img_arr, angle_54_deg)
axs[1].imshow(rot_img_54, cmap='gray')
axs[1].set_title('Rotated by 54°')

# Rotate by 213 degrees
rot_img_213 = my_img_rotation(img_arr, angle_213_deg)
axs[2].imshow(rot_img_213, cmap='gray')
axs[2].set_title('Rotated by 213°')

plt.show()
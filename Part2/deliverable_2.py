from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from my_corner_harris import my_corner_harris
from my_corner_harris import my_corner_peaks
import cv2

#set the filepath to the image file
filename = "im2.jpg"

#read the image into a PIL entity
img = Image.open(filename)

#keep only the Luminance component of the image
bw_img = img.convert("L")

#obtain the underlying np array
img_arr = np.array(bw_img,dtype=np.uint8)
img_arr_or= np.array(img,dtype=np.uint8)

#Put Threshold
threshold_value = 235
img_harris = np.where(img_arr < threshold_value, 0, img_arr)

sigma=30
window_size = round(4 * sigma)+1
blurred_img_harris = cv2.GaussianBlur(img_harris, (window_size,window_size), 30)

R=my_corner_harris(blurred_img_harris,0.05,20)
corners=my_corner_peaks(R,0.4)

plt.imshow(img_arr_or)
plt.axis('off')  # Hide the axes
plt.scatter(corners[1], corners[0], color='red', marker='s', s=6)  # Plot corners

# Show the plot
plt.show()

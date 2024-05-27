from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage import feature
from my_hough_transform import my_hough_transform
import cv2

#set the filepath to the image file
filename = "im2.jpg"

#read the image into a PIL entity
img = Image.open(filename)

#keep only the Luminance component of the image
bw_img = img.convert("L")

#obtain the underlying np array
img_arr = np.array(bw_img,dtype=np.uint8)
img_arr_or=np.array(img,dtype=np.uint8)

#Cut the image 
cropped_img = img_arr[50:6600, 100:5100]
img_arr_or = img_arr_or[50:6600, 100:5100]

#Put Threshold
threshold_value = 235
binary = cropped_img > threshold_value


#Edge detection
edges = feature.canny(binary)

#Hough Transform
d_theta=np.pi/200
d_rho=8
H,L,res =my_hough_transform(edges,8,np.pi/200,11)

plt.imshow(H, cmap='gray')
for rho, theta in L:
    theta_ind=int(theta/d_theta)
    rho_ind=int(rho/d_rho)
    plt.scatter(theta_ind,rho_ind, marker='x', color='red', s=15) 
   
plt.title('Hough Transform')
plt.xlabel('Theta ')
plt.ylabel('Rho')
plt.tight_layout()
plt.show()

# Draw lines on the original image
for rho, theta in L:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho 
    y0 = b * rho
    x1 = int(x0 + 10000 * (-b))
    y1 = int(y0 + 10000 * (a))
    x2 = int(x0 - 10000 * (-b))
    y2 = int(y0 - 10000 * (a))
    cv2.line(img_arr_or, (x1, y1), (x2, y2), (255, 0, 0), 5)

# Display the image with detected lines
plt.imshow(img_arr_or)
plt.tight_layout()
plt.show()
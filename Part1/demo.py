from PIL import Image
from global_hist_eq import perform_global_hist_equalization
from adaptive_hist_eq import perform_adaptive_hist_equalization
from adaptive_hist_eq import no_interference_transform
import numpy as np
import matplotlib.pyplot as plt

#set the filepath to the image file
filename = "input_img.png"

#read the image into a PIL entity
img = Image.open(filename)

#keep only the Luminance component of the image
bw_img = img.convert("L")

#obtain the underlying np array
img_array = np.array(bw_img,dtype=np.uint8)

#Kalesmata synarthsewn gia ton ypologismo twn eksisorrophmenwn eikonwn
equalization_img=perform_global_hist_equalization(img_array)
adaptive_equalization_img=perform_adaptive_hist_equalization(img_array,64,48)
adaptive_equalization_img_no_interference=no_interference_transform(img_array,64,48)


#Arxikh Eikona
plt.subplot(3, 2, 1)  
plt.imshow(img_array, cmap='gray')
plt.title('Original Image') 
plt.axis('off')

#Histogram arxikhs eikonas
plt.subplot(3, 2, 2)
plt.hist(img_array.flatten(), bins=256, range=(0,256), density=True, color='black')

#Eksisorrophmenh eikona
plt.subplot(3, 2, 3)  
plt.imshow(equalization_img, cmap='gray')  
plt.title('Equalized Image') 
plt.axis('off')

#Histogram eksisorrophmenhs eikonas
plt.subplot(3, 2, 4)
plt.hist(equalization_img.flatten(), bins=256, range=(0,256), density=True, color='black')

#Prosarmostikh Eksisorrophmenh eikona
plt.subplot(3, 2, 5) 
plt.imshow(adaptive_equalization_img, cmap='gray')  
plt.title('Adaptive Equalized Image') 
plt.axis('off')

#Histogram proeksisorrophmenhs eikonas
plt.subplot(3, 2, 6)
plt.hist(adaptive_equalization_img.flatten(), bins=256, range=(0,256), density=True, color='black')

plt.suptitle("Histograms- Image with Global and Adaptive Equalization", fontsize=16,fontweight='bold')
plt.show()  #Emfanish Plot


#Subplot parathrhshs asynexeias
plt.subplot(1,2,1)
plt.imshow(adaptive_equalization_img, cmap='gray')  
plt.title('With Interpolation of neighboring transformations') 
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(adaptive_equalization_img_no_interference, cmap='gray')  
plt.title('Without Interpolation of neighboring transformations') 
plt.axis('off')

plt.suptitle("Adaptive Histogram Equalization")
plt.show()  #Emfanish Plot

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from my_hough_transform import my_hough_transform
from my_corner_harris import my_corner_harris
from my_corner_harris import my_corner_peaks
from skimage import feature
import cv2
from scipy.spatial import cKDTree

#meiwnei ta corners sta osa prepei na einai
def merge_close_points(coordinates, threshold):
    tree = cKDTree(coordinates.T)
    merged_indices = set()
    merged_coordinates = []

    for i, current_point in enumerate(coordinates.T):
        if i in merged_indices:
            continue

        neighbors = tree.query_ball_point(current_point, threshold)
        merged_point = np.mean(coordinates[:, neighbors], axis=1)
        merged_coordinates.append(merged_point)
        merged_indices.update(neighbors)

    return np.array(merged_coordinates).T

#briskei an ena shmeio anhkei se mia eytheia h oxi
def point_on_line(point, rho, theta, tolerance_rho, tolerance_theta):
    x, y = point
    rho_calc = y * np.cos(theta) + x * np.sin(theta)
    theta_calc = theta
    return np.abs(rho - rho_calc) <= tolerance_rho and np.abs(theta - theta_calc) <= tolerance_theta

#dhmioyrgei mia lista twn eytheiwn poy dierxontai apo ena shmeio 
def find_lines_for_point(L, point, tolerance_rho, tolerance_theta):
    lines_for_point = []
    
    for line_idx, (rho, theta) in enumerate(L):
        if point_on_line(point, rho, theta, tolerance_rho, tolerance_theta):
            lines_for_point.append(line_idx)
    
    return lines_for_point

#set the filepath to the image file
filename = "im1.jpg"

#read the image into a PIL entity
img = Image.open(filename)

#keep only the Luminance component of the image
bw_img = img.convert("L")

#obtain the underlying np array
img_arr = np.array(bw_img,dtype=np.uint8)
img_arr_or=np.array(img,dtype=np.uint8)

#Put Threshold
threshold_value = 235
binary = img_arr > threshold_value

edges = feature.canny(binary)

#Hough Transform
H,L,res =my_hough_transform(edges,8,np.pi/200,11)

img_harris = np.where(img_arr < threshold_value, 0, img_arr)

sigma=30
window_size = round(4 * sigma)+1
blurred_img_harris = cv2.GaussianBlur(img_harris, (window_size,window_size), 30)

#Eyresh corners
R=my_corner_harris(blurred_img_harris,0.05,20)
corners=my_corner_peaks(R,0.4)

#meiwsh corners stis real
corners=merge_close_points(np.array(corners), 100)

line_indices_for_corners = []
for corner in corners.T:
    lines_for_point = find_lines_for_point(L, corner,100,0.6)
    line_indices_for_corners.append(lines_for_point)



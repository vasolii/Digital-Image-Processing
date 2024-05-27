import numpy as np
import cv2

def my_corner_harris(img: np.ndarray,k: float,sigma: float):
    # Compute derivatives
    Ix = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    Iy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    
    # Gaussian blur
    window_size = round(4 * sigma)+1
    Ix2 = cv2.GaussianBlur(Ix**2, (window_size, window_size), sigma)
    Iy2 = cv2.GaussianBlur(Iy**2, (window_size, window_size), sigma)
    Ixy = cv2.GaussianBlur(Ix*Iy, (window_size, window_size), sigma)
    
    # Compute M matrix
    det_M = Ix2 * Iy2 - Ixy**2
    trace_M = Ix2 + Iy2
    R = det_M - k * trace_M**2
    
    return R

def my_corner_peaks(harris_response: np.ndarray,rel_threshold: float):
    thr=harris_response.max()*rel_threshold
    corners = np.where(harris_response > thr)
    return corners

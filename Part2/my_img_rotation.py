import numpy as np
import math

def my_img_rotation(img: np.ndarray, angle: float):
    # Initial dimensions
    h, w = img.shape[:2]

    c = math.cos(angle)
    s = math.sin(angle)

    # New dimensions
    new_w = int(w * abs(c) + h * abs(s))
    new_h = int(h * abs(c) + w * abs(s))

    # Initial center
    x_center = w / 2
    y_center = h / 2

    # New center
    new_x_center = new_w / 2
    new_y_center = new_h / 2

    # Initialize the rotated image
    if len(img.shape) == 3:
        rot_img = np.zeros((new_h, new_w, img.shape[2]), dtype=img.dtype)
    else:
        rot_img = np.zeros((new_h, new_w), dtype=img.dtype)

    # Generate grid of coordinates in the new image
    new_x, new_y = np.meshgrid(np.arange(new_w), np.arange(new_h))
    
    # Calculate the corresponding coordinates in the original image
    x_rot = new_x - new_x_center
    y_rot = new_y - new_y_center

    x = c * x_rot - s * y_rot + x_center
    y = s * x_rot + c * y_rot + y_center

    # Floor and ceil values
    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)

    x1 = x0 + 1
    y1 = y0 + 1

    x0 = np.clip(x0, 0, w - 1)
    x1 = np.clip(x1, 0, w - 1)
    y0 = np.clip(y0, 0, h - 1)
    y1 = np.clip(y1, 0, h - 1)

    # Get pixel values
    Ia = img[y0, x0]
    Ib = img[y0, x1]
    Ic = img[y1, x0]
    Id = img[y1, x1]

    # Average the four pixel values
    if len(img.shape) == 3:
        rot_img[:, :, :] = (Ia/4 + Ib/4 + Ic/4 + Id/4).astype(img.dtype)
    else:
        rot_img[:, :] = (Ia/4 + Ib/4 + Ic/4 + Id/4).astype(img.dtype)

    rot_img[(x < 0) | (x >= w) | (y < 0) | (y >= h)] = [0, 0, 0] if len(img.shape) == 3 else 0

    return rot_img


    

    
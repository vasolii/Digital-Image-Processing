import numpy as np
import math

def my_hough_transform(img_binary: np.ndarray, d_rho: int, d_theta: float, n: int):
    N1, N2 = img_binary.shape

    theta = np.arange(0, 2*np.pi, d_theta)
    ro = np.arange(0, int(math.sqrt(N1**2 + N2**2)), d_rho)

    H = np.zeros((len(ro), len(theta)), dtype=int)

    for n2 in range(N2):
        for n1 in range(N1):
            if img_binary[n1][n2] !=0 :
                for j in range (len(theta)):
                    tnew=(2*theta[j]+d_theta)/2 
                    ronew = n2 * np.cos(tnew) + n1 * np.sin(tnew)
                    if ronew>=0:
                        rho_index = int(ronew//d_rho)
                        H[rho_index][j] += 1

    # Find indices of top N elements
    indices = np.argpartition(H.flatten(), -n)[-n:]
    indices= np.column_stack(np.unravel_index(indices, H.shape))
    
    # Extract rho and theta values corresponding to top N indices
    L = np.array([[ro[index[0]], theta[index[1]]] for index in indices])
     
    # Calculate the number of points not belonging to the top N lines
    res = np.sum(img_binary) - np.sum(H[indices[:, 0], indices[:, 1]])

    return H, L,res

                 
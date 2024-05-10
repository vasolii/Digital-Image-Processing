import numpy as np

def get_equalization_transform_of_img(img_array):
    L=256
    #Histogram
    hist=custom_hist(img_array,L)
    p = hist / float(np.sum(hist)) #Ypologismos ths pithanothtas emfanishs kathe epipedoy fwteinothtas
    u=np.zeros(L)
    y=np.zeros(L, dtype=np.uint8)
    u[0]=p[0]
    y[0]=0
    #ypologismos metasxhmatismoy gia ola ta epipeda fwteinothtas apo 0-256
    for k in range(1,L,1):
        #Typoi thewrias
        u[k]=u[k-1]+p[k]
        y[k]=round((u[k]-u[0])*(L-1)/(1-u[0]))
    return y   

def perform_global_hist_equalization(img_array):
    equalized_img=np.zeros((img_array.shape[0],img_array.shape[1]),dtype=np.uint8) #Arxikopoihsh eksisorrophmenoy pinaka
    equalized_transform=get_equalization_transform_of_img(img_array)
    #Loupa gia kathe pixel tou image
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            equalized_img[i][j]=equalized_transform[img_array[i][j]]        
    return equalized_img

def custom_hist(arr, minlength):
    """H synarthsh ayth briskei tis monadikes times kai ton arithmo emfanishs toys ston pinaka array kai ta metaferei se enan
    pinaka mhkous minlength"""
    unique_values, counts = np.unique(arr.ravel(), return_counts=True) #H ravel kanei ton pinaka arr monodiastato
    result = np.zeros(minlength, dtype=int)
    result[unique_values] = counts
    return result
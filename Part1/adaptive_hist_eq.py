import numpy as np
import math
from global_hist_eq import get_equalization_transform_of_img

def calculate_eq_transformations_of_regions(img_array,region_len_h,region_len_w):
    region_to_eq_transform = {} #dict
    height, width = img_array.shape #diastaseis image

    """To parakatw loop exei ws stoxo ton ypologismo twn diastasewn toy kathe region kai me thn bohtheia ths synarthshs
    get_equalization_transform_of_img toy metasxhmatismoy toy, na ypologizetai o metasxhmatismos kai na prostithetai 
    sto parapanw arxikopoihmeno dictionary"""

    for i in range(0, height, region_len_h):
        for j in range(0, width, region_len_w):

            region = (i, j) #tuple
            #Diastaseis toy region
            region_end_h = i + region_len_h -1
            region_end_w = j + region_len_w -1
            region_array = img_array[i:region_end_h, j:region_end_w]
            
            eq_transform = get_equalization_transform_of_img(region_array)
            
            region_to_eq_transform[region] = eq_transform
    return region_to_eq_transform   

def perform_adaptive_hist_equalization(img_array,region_len_h,region_len_w):
    equalized_img=np.zeros((img_array.shape[0],img_array.shape[1]), dtype=np.uint8) #Arxikopoihsh eksisorrophmenoy pinaka
    height, width = img_array.shape #diastaseis image
    regions_transform=calculate_eq_transformations_of_regions(img_array,region_len_h,region_len_w) 
    #Loupa gia kathe pixel tou image
    for i in range(height):
        for j in range(width):   
            equalized_img[i][j]=interference_transform((i,j),img_array,region_len_h,region_len_w,regions_transform)
    return  equalized_img     
  
#Ksexwiristh synarthsh gia ton ypologismo toy metasxhmatismenoy pixel xwrista
def interference_transform(pixel,img_array,region_len_h,region_len_w,regions_transform):    
    #Outer points
    if (pixel[0]<=region_len_h/2 or pixel[0]>=img_array.shape[0]-region_len_h/2 or pixel[1]<=region_len_w/2 or pixel[1]>=img_array.shape[1]-region_len_w/2):

        """Ta parakatw counts tha bohthsoyn gia thn eyeresh tou region to opoio anhkei to shmeio"""
        count_x_region=math.ceil(pixel[0]/region_len_h)
        count_y_region=math.ceil(pixel[1]/region_len_w)

        """O parakatw elegxos ginetai gia na kalyfthei h periptwsh twn outer points poy anhkoyn se regions ta opoia orizontai ws (0,y) kai (x,0) 
        An kratiotan h timh mhden,to key toy zhtoymenoy region_transform tha htan lathos (Kai arnhtiko)"""
        if count_x_region==0:
            count_x_region=1
        if count_y_region==0:
            count_y_region=1  

        #Eyresh zhtoymenoy metasxhmatismoy      
        t=regions_transform[(count_x_region-1)*region_len_h,(count_y_region-1)*region_len_w]
        y=t[img_array[pixel[0],pixel[1]]] 

    #Inner points
    else:  
        #Eyresh geitonikwn regions
        """Ta parakatw counts tha bohthsoyn gia thn eyeresh toy kontinoteroy kentroy  +,+. To +,+ isxyei giati ginetai xrhsh ths math.ceil h 
        opoia strogylopoiei to apotelesma pros ta panw, ston amesws epomeno akeraio"""
        count_x_centers=math.ceil((pixel[0]-region_len_h/2)/region_len_h)
        count_y_centers=math.ceil((pixel[1]-region_len_w/2)/region_len_w)  
        #Eyresh arxika C+,+ kentroy me bash ton parapanw ypologismo 
        center_r_plus=(region_len_h/2+count_x_centers*region_len_h,region_len_w/2+count_y_centers*region_len_w) 

        """Ypologismos twn ypoloipwn kentrwn me bash to panw deksia, me thn logikh oti kseroyme thn statherh apostash metaksy kentrwn (region_len_h kai region_len_w)
        kai oti ta kentra sxhmatizoyn parallhlogrammo (kathta metaksy toys)"""
        center_r_plus_minus=(center_r_plus[0],center_r_plus[1]-region_len_w)
        center_r_minus=(center_r_plus[0]-region_len_h,center_r_plus[1]-region_len_w)
        center_r_minus_plus=(center_r_plus[0]-region_len_h,center_r_plus[1])
                
        a=(pixel[1]-center_r_minus[1])/(center_r_plus[1]-center_r_minus[1])  
        b=(pixel[0]-center_r_minus[0])/(center_r_plus[0]-center_r_minus[0])  

        #metasxhmatismoi twn getonikwn regions
        "Oi gwnies poy kathorizoyn kathe region ypologizontai me thn bohtheia toy kentroy kai gnvrizontas tis diastaseis toy parallhlogramoy"
        t_minus = regions_transform[(center_r_minus[0]-region_len_h/2,center_r_minus[1]-region_len_w/2)]
        t_minus_plus = regions_transform[(center_r_minus_plus[0]-region_len_h/2,center_r_minus_plus[1]-region_len_w/2)]
        t_plus_minus = regions_transform[(center_r_plus_minus[0]-region_len_h/2,center_r_plus_minus[1]-region_len_w/2)]
        t_plus = regions_transform[(center_r_plus[0]-region_len_h/2,center_r_plus[1]-region_len_w/2)]

        #Teliko apotelesma metasxhmatismoy       
        y=(1-a)*(1-b)*t_minus[img_array[pixel[0],pixel[1]]]\
            +(1-a)*b*t_plus_minus[img_array[pixel[0],pixel[1]]]\
                +a*(1-b)*t_minus_plus[img_array[pixel[0],pixel[1]]]\
                    +a*b*t_plus[img_array[pixel[0],pixel[1]]]
    return y 
 
"H synarthsh ayth ylopoieitai etsi wste na parathrhthei sthn periptwsh mh xrhshs ths parembolhs, h asynexeia metaksy twn regions"
def no_interference_transform(img_array,region_len_h,region_len_w):
    equalized_img=np.zeros((img_array.shape[0],img_array.shape[1]), dtype=np.uint8) #Arxikopoihsh eksisorrophmenoy pinaka
    height, width = img_array.shape #diastaseis image
    regions_transform=calculate_eq_transformations_of_regions(img_array,region_len_h,region_len_w) 
    #Loupa gia kathe pixel tou image
    for i in range(height):
        for j in range(width):
            """Ta parakatw counts tha bohthsoyn gia thn eyeresh tou region to opoio anhkei to shmeio"""
            count_x_region=math.ceil(i/region_len_h)
            count_y_region=math.ceil(j/region_len_w)

            """O parakatw elegxos ginetai gia na kalyfthei h periptwsh twn outer points poy anhkoyn se regions ta opoia orizontai ws (0,y) kai (x,0) 
            An kratiotan h timh mhden,to key toy zhtoymenoy region_transform tha htan lathos (Kai arnhtiko)"""
            if count_x_region==0:
                count_x_region=1
            if count_y_region==0:
                count_y_region=1  

            #Eyresh zhtoymenoy metasxhmatismoy      
            t=regions_transform[(count_x_region-1)*region_len_h,(count_y_region-1)*region_len_w]
            equalized_img[i][j]=t[img_array[i,j]] 
    return  equalized_img    
#!/usr/bin/env python 
                       # DETECTING A QR CODE AND PRINTING THE COORDINATES OF ITS CORNERS


"""
    # Some part of the code, i.e., the part of FOR loop block of DECODE() function,
    # is taken from and then modified from the website :
    # https://github.com/cuicaihao/Webcam_QR_Detector/blob/master/Lab_01_QR_Bar_Code_Detector_Basic.ipynb
"""

                # ************** IN THE FINAL IMAGE, ORIGIN = TOP_LEFT *************** #



from pyzbar.pyzbar import decode    # Pyzbar Library
#from PIL import Image               # Library not required here
import  cv2                         # OpenCV Library
import numpy as np                  # Numpy Library
from matplotlib import pyplot as plt# MatPlotLib library

cap = cv2.VideoCapture(0)#'xt.avi')    # 'xt.avi' is the test video


# Saving the output video
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('q_out.avi', fourcc, 20.0, (640,840))
# this above last argument (resolution) should match that of input. else, error
# So, inorder to eliminate any errors, use the following commands:


frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
 
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))


d = 1                               # A simple counter
while(cap.isOpened()):

    tex = []                        # 'tex' holds the final points 
    ret, img = cap.read()           # 'ret' tells whether a frame exists or not
    
    if ret==True:
        print('-------------Frame ',d, ' --------------')
        print("printing hull's points")

        # Decode() is an inbuilt 'pyzbar' library function 
        for code in decode(img):
            points = code.polygon
            # If the points do not form a quad, find convex hull
            if len(points) > 4 : 
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else : 
                hull = points       # if it's a Quadrilateral
                
            # Number of points in the convex hull
            n = len(hull)
            tex = hull              # here 'tex' stores the  corner points
            
            # Draw the convex hull
            for j in range(0,n):
                print(hull[j])
                cv2.line(img, hull[j], hull[ (j+1) % n], (255,0,0), 2)  # 'line' joins the corners

        # Drawing the Text - Coordinates
        font = cv2.FONT_HERSHEY_SIMPLEX
        x = 1                       # again a counter
        for i in tex:
            cv2.putText(img, str(i), i, font, 0.4, (0,0,255), 1, cv2.LINE_AA)
            x+=1

        out.write(img)              # Saving the frame
            
        cv2.imshow('\8_8/',img)     # Displaying the frame
        
        k = cv2.waitKey(5) & 0xFF   # waitKey(*) -> '*' tells us the speed of the video capture in millisec
        if k==27:           
            break                   # Press 'Esc' to exit
    else:
        break
    d+=1

# Release cap and close all windows
cap.release()
out.release()
cv2.destroyAllWindows()


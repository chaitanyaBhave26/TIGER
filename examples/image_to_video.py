import glob
import os
import cv2

#DEFINE PATTERN THAT DESCRIBES ALL IMAGES --> * CAN BE FILLED WITH ANYTHING
file_names = '2D/2d_fancy_*.png'
video_file_name = '2D/2d_fancy.avi'

#USE GLOB TO READ ALL FILES WITH GIVEN PATTERN
img_name_list = glob.glob(file_names)
#SORT BY MODIFIED DATE TO ENSURE FRAMES ARE IN RIGHT ORDER
img_name_list.sort(key=os.path.getmtime)

frames = [cv2.imread(name) for name in img_name_list]

h,w,c = frames[0].shape

fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter(video_file_name,fourcc,20,(w,h))

for frame in frames:
    out.write(frame)

out.release()

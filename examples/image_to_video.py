import glob
import os
import cv2

#DEFINE BASE NAME FOR FILES
file_names = 'temp/1d_exodus_line_plot_'
#NAME OF VIDEO FILE TO GENERATE
video_file_name = '2D/2D_render.avi'
#PARAMETERS FOR VIDEO
n_frames = 200
fps = 20

frames =[]
for i in range(n_frames):
    frames += [Image.open(file_names+str(i)+'.png')]

#GET DIMENSIONS OF FRAME
h,w,c = frames[0].shape

#FOURCC OBJECT ENCODES THE IMAGE SEQUENCE INTO REQUIRED FORMAT
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
#VIDEO WRITER OBJECT TO ACTUALLY WRITE THE VIDEO
out = cv2.VideoWriter(video_file_name,fourcc,fps,(w,h))

#WRITE FRAMES TO VIDEO FILE
for frame in frames:
    out.write(frame)

#RELEASE VIDEO WRITER OBJECT (NOT NECESSARY BUT GOOD PRACTICE)
out.release()

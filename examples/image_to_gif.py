from PIL import Image
import glob
import os

#DEFINE BASE NAME FOR FILES
file_names = 'temp/1d_exodus_line_plot_'
#NAME OF VIDEO FILE TO GENERATE
gif_file_name = '2D/2D_render.gif'
#PARAMETERS FOR VIDEO
n_frames = 200
fps = 20

frames =[]
for i in range(n_frames):
    frames += [Image.open(file_names+str(i)+'.png')]

#EACH FRAME LASTS 1000/FPS MILLISECONDS
frame_duration = 1000/fps
#SAVE PIL.IMAGE SEQUENCE INTO A GIF --> TURN ON OPTIMIZE FOR SMALLER FILE SIZE
frames[0].save(gif_file_name,save_all=True,optimize=False,append_images=frames[1:],loop=0,duration=frame_duration)

from PIL import Image
import glob
import os

#DEFINE PATTERN THAT DESCRIBES ALL IMAGES --> * CAN BE FILLED WITH ANYTHING
file_names = '2D/2d_fancy_*.png'

#USE GLOB TO READ ALL FILES WITH GIVEN PATTERN
img_name_list = glob.glob(file_names)
#SORT BY MODIFIED DATE TO ENSURE FRAMES ARE IN RIGHT ORDER
img_name_list.sort(key=os.path.getmtime)

frames = [Image.open(img_name) for img_name in img_name_list]

frames[0].save('2D/2d_render.gif',save_all=True,optimize=False,append_images=frames[1:],loop=0,duration=50) ##Duration is frame duration in ms. 20 fps ==>> 50 ms duration

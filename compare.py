import metrics as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2 
from matplotlib import image
from skimage import color
from skimage import io
from scipy.ndimage import zoom
from PIL import Image
import numpy
import numpy as np
from matplotlib import pyplot as plt

"""
srcImage = Image.open("C:\\Users\\stefa\\OneDrive\\Desktop\\save\\batiments_reels_2002.01.01.geojson.png")

image2=Image.open("C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\resultats\\batiments_reels_2019.01.25.geojson.png")


im_gray = np.array(Image.open("C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\resultats\\batiments_reels_2019.01.25.geojson.png").convert('L'))



img = cv2.imread("C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\resultats\\buildings_simu_2019.geojson.png",2)
ret, bw_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

img2 = cv2.imread("C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\resultats\\buildings_simu_2019.geojson.png",2)
ret2, bw_img2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

bw = bw_img/255
bw2= bw_img2/255


final = bw - bw2




cv2.imshow("Binary Image",srcImage)
cv2.waitKey(0)
cv2.destroyAllWindows()


"""






from PIL import Image
  
from PIL import Image, ImageDraw, ImageFilter



"""
im_rgb= Image.open("C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\resultats\\batiments_reels_2019.01.25.geojson.png")

im_rgba = im_rgb.copy()
im_rgba.putalpha(128)
im_rgba.save('pillow_putalpha_solid.png')
plt.imshow(im_rgba)


im_a = Image.open("C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\resultats\\map.png").convert('L').resize(im_rgb.size)
im_a.save('pillow_putalpha_horse.png')




im_rgba = im_rgb.copy()
im_rgba.putalpha(im_a)
im_rgba.save('pillow_putalpha_horse.png')

"""

import cv2
import numpy as np

img2 = cv2.imread("C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\resultats\\batiments_simulation_2020.01.15.geojson.png")
img1 = cv2.imread("C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\resultats\\map.png")
dst = cv2.addWeighted(img1, 1, img2, 0.4, 0)

img_arr = np.hstack((img1, img2))

cv2.imwrite('C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\resultats\\Comp.jpg', img_arr) 
cv2.imwrite('C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\resultats\\Blend.jpg', dst) 
cv2.waitKey(0)
cv2.destroyAllWindows()
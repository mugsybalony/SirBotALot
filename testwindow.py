
from PIL import Image
import pygame
import cv2
import pyautogui
from pytesseract import image_to_string
import time



#img = ImageGrab.grab(bbox=(260, 222, 300, 75))
#img.save('smallscreen.png')

t0 = time.time()
img = pyautogui.screenshot(region=(350,191,100,30))
img.save('pot.png')

pot =  image_to_string(Image.open('pot.png'))
t1 = time.time()
t = t1-t0

'0123456789'



print pot, ' pot found in %s seconds' %t


#img = cv2.imread("screen.png")
#crop_img = img[222:295,260:560]
#cv2.imwrite('smallscreen.png',crop_img)
#cv2.imshow('crop_img', crop_img)
#cv2.waitKey(0)







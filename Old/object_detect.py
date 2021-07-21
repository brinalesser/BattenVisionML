import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def detect(im):
	im_rgb = cv.cvtColor(im, cv.COLOR_BGR2RGB)
	im_gs = cv.cvtColor(im, cv.COLOR_BGR2GRAY)


	#find battens
	batten_data = cv.CascadeClassifier("Images/cascade/cascade.xml")
	found = batten_data.detectMultiScale(im_gs, minSize=(20,20))

	amount_found = len(found)
	print(amount_found)
	
	#draw rectangle around object
	if(amount_found != 0):
		for(x, y, width, height) in found:
			cv.rectangle(im_rgb, (x,y), ((x+height), (y+width)), (0,255,0), 5)

	found = batten_data.detectMultiScale(im_gs, minSize=(200,20))

	amount_found = len(found)
	print(amount_found)
	
	#draw rectangle around object
	if(amount_found != 0):
		for(x, y, width, height) in found:
			cv.rectangle(im_rgb, (x,y), ((x+height), (y+width)), (0,255,0), 5)

	plt.subplot(1, 1, 1)
	plt.imshow(im_rgb)
	plt.show()
	cv.waitKey(0)
	cv.destroyAllWindows()

if __name__=='__main__':
	im = cv.imread("Images/pos_img/vid5_frame105.jpg")
	detect(im)

	
	

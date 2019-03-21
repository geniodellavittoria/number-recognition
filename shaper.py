import cv2
import time
import numpy as np

##################
DELAY = 0.02
USE_CAM = 1
IS_FOUND = 0

MORPH = 7
CANNY = 250
##################
_width  = 600.0
_height = 420.0
_margin = 0.0
##################

if USE_CAM: video_capture = cv2.VideoCapture(0)

corners = np.array(
	[
		[[  		_margin, _margin 			]],
		[[ 			_margin, _height + _margin  ]],
		[[ _width + _margin, _height + _margin  ]],
		[[ _width + _margin, _margin 			]],
	]
)

pts_dst = np.array( corners, np.float32 )

while True :

	if USE_CAM :
		ret, rgb = video_capture.read()
	else :
		ret = 1
		rgb = cv2.imread( "opencv.jpg", 1 )

	if ( ret ):

		

				else : pass

		#cv2.imshow( 'closed', closed )
		#cv2.imshow( 'gray', gray )
		cv2.namedWindow( 'edges')
		cv2.imshow( 'edges', edges )

		cv2.namedWindow( 'rgb')
		cv2.imshow( 'rgb', rgb )

		if IS_FOUND :
			cv2.namedWindow( 'out')
			cv2.imshow( 'out', out )

		if cv2.waitKey(27) & 0xFF == ord('q') :
			break

		if cv2.waitKey(99) & 0xFF == ord('c') :
			current = str( time.time() )
			cv2.imwrite( 'ocvi_' + current + '_edges.jpg', edges )
			cv2.imwrite( 'ocvi_' + current + '_gray.jpg', gray )
			cv2.imwrite( 'ocvi_' + current + '_org.jpg', rgb )
			print ("Pictures saved")

		time.sleep( DELAY )

	else :
		print ("Stopped")
		break

if USE_CAM : video_capture.release()
cv2.destroyAllWindows()


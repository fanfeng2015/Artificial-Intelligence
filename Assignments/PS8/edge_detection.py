from skimage import io
from skimage import feature
from skimage.color import rgb2gray
from skimage.filters import roberts
from skimage.filters import sobel

# original image
img = io.imread('yale.png')
io.imshow(img)
io.show()

# greyscale image
grey_img = rgb2gray(img)
io.imshow(grey_img)
io.show()

# Sobel Operator
sobel_edge = sobel(grey_img)
io.imshow(sobel_edge)
io.show()

# Robot's Cross
robert_cross_edge = roberts(grey_img)
io.imshow(robert_cross_edge)
io.show()

# the Canny edge detector
canny_edge = feature.canny(grey_img)
io.imshow(canny_edge)
io.show()


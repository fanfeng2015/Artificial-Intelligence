import numpy as np
from skimage import io
from skimage import measure

# original image
img = io.imread('object.jpg')
io.imshow(img)
io.show()

# binary images
redImage = img[:, :, 0]
greenImage = img[:, :, 1]
blueImage = img[:, :, 2]

redBinary = np.logical_and(redImage > 130, np.logical_and(greenImage < 100, blueImage < 130))
greenBinary = np.logical_and(redImage < 121, np.logical_and(greenImage > 125, blueImage < 130))
blueBinary = np.logical_and(redImage < 100, np.logical_and(greenImage < 170, blueImage > 140))
yellowBinary = np.logical_and(redImage > 125, np.logical_and(greenImage > 125, blueImage < 125))

io.imshow(redBinary)
io.show()
io.imshow(greenBinary)
io.show()
io.imshow(blueBinary)
io.show()
io.imshow(yellowBinary)
io.show()

# connected components (region growing)
redTagged, redN = measure.label(redBinary, neighbors = 8, return_num = True)
greenTagged, greenN = measure.label(greenBinary, neighbors = 8, return_num = True)
blueTagged, blueN = measure.label(blueBinary, neighbors = 8, return_num = True)
yellowTagged, yellowN = measure.label(yellowBinary, neighbors = 8, return_num = True)

print(redN)
print(greenN)
print(blueN)
print(yellowN)

# compute the boundary (max/min row/col) and centroid (average row/col)
def computeRegionStatistics(taggedImage, region):
	rows = []
	cols = []
	for i in range(len(taggedImage)):
		for j in range(len(taggedImage[0])):
			if taggedImage[i][j] == region:
				rows.append(i)
				cols.append(j)
	return round(sum(rows)/len(rows), 2), round(sum(cols)/len(cols), 2), max(rows), max(cols), min(rows), min(cols)

print(computeRegionStatistics(redTagged, 1))
print(computeRegionStatistics(redTagged, 2))
print(computeRegionStatistics(greenTagged, 1))
print(computeRegionStatistics(greenTagged, 2))
print(computeRegionStatistics(blueTagged, 1))
print(computeRegionStatistics(blueTagged, 2))
print(computeRegionStatistics(yellowTagged, 1))
print(computeRegionStatistics(yellowTagged, 2))



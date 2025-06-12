import cv2
import numpy as np

def detect_craters_and_mountains(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.medianBlur(gray, 5)

    craters = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1.2, 20,
                               param1=50, param2=30, minRadius=5, maxRadius=30)

    edges = cv2.Canny(blurred, 100, 200)
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=5)
    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)

    mountain_mask = (gradient_magnitude > 150).astype(np.uint8)

    h, w = gray.shape
    grid = np.zeros((h, w), dtype=np.uint8)

    if craters is not None:
        craters = np.uint16(np.around(craters))
        for i in craters[0, :]:
            cv2.circle(grid, (i[0], i[1]), i[2], 1, -1)

    grid[mountain_mask == 1] = 1
    return grid

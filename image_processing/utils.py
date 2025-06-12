import cv2
import numpy as np
from PIL import Image

def draw_path(image, path, current_pos, destination):
    vis = image.copy()
    for y, x in path:
        vis[y, x] = [0, 255, 0]
    if current_pos:
        y, x = current_pos
        cv2.circle(vis, (x, y), 4, (0, 0, 255), -1)
    if destination:
        y, x = destination
        cv2.circle(vis, (x, y), 4, (255, 0, 0), -1)
    return Image.fromarray(vis)

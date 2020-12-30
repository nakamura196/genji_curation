import cv2
import numpy as np

def find_rect_of_target_color(image):
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
  h = hsv[:, :, 0]
  s = hsv[:, :, 1]
  mask = np.zeros(h.shape, dtype=np.uint8)
  mask[((h < 20) | (h > 200)) & (s < 80)] = 255
  contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  rects = []
  for contour in contours:
    approx = cv2.convexHull(contour)
    rect = cv2.boundingRect(approx)
    rects.append(np.array(rect))
  return rects

img = cv2.imread("12_2_org.jpg")
rects = find_rect_of_target_color(img)
if len(rects) > 0:
    
    rect = max(rects, key=(lambda x: x[2] * x[3]))
    cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2)

cv2.imwrite("check.jpg", img)
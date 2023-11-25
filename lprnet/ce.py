import cv2

image = cv2.imread('ces/label.png')
yuantu = cv2.imread('ces/img.png')

img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 将mask转换为灰度图
ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)  # 大于0的部分变为白，小于等于0的部分变黑
img1_bg = cv2.bitwise_and(yuantu, yuantu, mask=mask)  # 按位与，0直接变黑，原图贴上白色部分不变

cv2.imshow("111", img1_bg)
cv2.waitKey(0)

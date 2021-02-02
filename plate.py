
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract"


image = cv2.imread('auto001.jpg')
#
# Resize the image - change width to 300
#image = imutils.resize(image, width=300)


cv2.imshow("Original Image", image)
cv2.waitKey(0)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("1 - gri image", gray)
cv2.waitKey(0)


#gray = cv2.bilateralFilter(gray, 11, 17, 17)
gray = cv2.blur(gray, (3, 3))
cv2.imshow("2 - blur image", gray)
cv2.waitKey(0)


edged = cv2.Canny(gray, 120, 200)
cv2.imshow("3 - canny image", edged)
cv2.waitKey(0)


cnts, new  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


img1 = image.copy()
cv2.drawContours(img1, cnts, -1, (0,255,0), 3)
cv2.imshow("4- all counters.", img1)
cv2.waitKey(0)

#sort contours based on their area keeping minimum required area as '30' (anything smaller than this will not be considered)
cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:20]
plate = None

# Top 30 Contours
img2 = image.copy()
cv2.drawContours(img2, cnts, -1, (0,255,0), 3)
cv2.imshow("5- Big 20 Contours", img2)
cv2.waitKey(0)


count = 0
idx =7
for c in cnts:
        area = cv2.contourArea(c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.07 * peri, True)

        if len(approx) == 4:
            plate = approx
            x, y, w, h = cv2.boundingRect(c)
            new_img = gray[y:y + h, x:x + w]
            text = pytesseract.image_to_string(new_img, config='--psm 11')


            cv2.imshow('plate', new_img)


            break


#
cv2.drawContours(image, [plate], -1, (0,255,0), 3)
cv2.imshow("final", image)


print("plate number is :", text)

cv2.waitKey(0)
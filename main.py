import cv2 as cv
import numpy as np

def getCount(img, imgCont):

    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 5000:
            cv.drawContours(imgCont, cnt, -1, (255, 0, 255), 7)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
            x = len(approx)
            sx = 0
            sy = 0
            for it in approx:
                sx = sx + it[0][0]
                sy = sy + it[0][1]
            midx = int(sx/x)
            midx = midx - 25
            midy = int(sy/x)
            if x == 3:
                cv.putText(imgCont, "Tri", (midx, midy), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,0,0))
            elif x == 10:
                cv.putText(imgCont, "Star", (midx, midy), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,0,0))
            elif x == 4:
                list_x_len = []
                list_y_len = []
                for i in range(1,3):
                    list_x_len.append(approx[i][0][0]-approx[i-1][0][0])
                    list_y_len.append(approx[i][0][1]-approx[i-1][0][1])
                a = (list_x_len[0]*list_x_len[0]) + (list_y_len[0]*list_y_len[0])
                b = (list_x_len[1]*list_x_len[1]) + (list_y_len[1]*list_y_len[1])
                print(abs(a - b))
                if abs(a - b)<1100:
                    cv.putText(imgCont, "Square", (midx, midy), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,0,0))
                else:
                    cv.putText(imgCont, "Rect", (midx, midy), cv.FONT_HERSHEY_COMPLEX, 0.8, (0,0,0))
            else:
                cv.putText(imgCont, "Circ", (midx, midy), cv.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0))



img = cv.imread("shapes.jpg")
scale_percent = 50
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width,height)
resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)

imgBlur = cv.GaussianBlur(resized, (7, 7), 1)
imgGray = cv.cvtColor(imgBlur, cv.COLOR_BGR2GRAY)

imgCanny = cv.Canny(imgGray, 140, 255)
kernel = np.ones((5,5))
imgDil = cv.dilate(imgCanny, kernel, iterations=1)

imgContour = resized.copy()
getCount(imgDil, imgContour)

cv.imshow("Image", imgContour)
cv.waitKey(0)

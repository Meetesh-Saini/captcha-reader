import sys
from PIL import Image
import numpy as np
import pytesseract
import cv2

parentDir = "/home/meetesh/Desktop/programs/VS/OCR/Captcha/upload"

def cap(name, iter_c=0):
    s = Image.open(parentDir+"/tests/"+name)
    s = s.convert('RGB')
    key = [
        [0.5, 1, 0],
        [4, 0, 7],
        [4.2, 5, 1]
    ]

    for i in range(s.size[0]):
        for j in range(s.size[1]):
            s.putpixel((i, j), tuple(
                map(int, tuple(np.matmul(key, s.getpixel((i, j)))))))

    filename = f"{parentDir}/tests/capTemp.png"
    s.save(filename)

    img = cv2.imread(filename)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.bilateralFilter(gray_img, 9, 75, 75)

    for i in img:
        for j in range(len(i)):
            if i[j] > 127:
                i[j] = 255
            else:
                i[j] = 0

    kernel2 = np.ones((5, 5), np.float32) / 30

    img = cv2.filter2D(src=img, ddepth=-1, kernel=kernel2)

    text = pytesseract.image_to_string(img)
    return text.strip()

# running tests
correct = ["5MG39A", "ADA8VG", "D8795T", "L3EWC1", "NFHNUW", "TNZRHW", "AID6VY", "GKEBP6", "R1E45A", "WUXNS5",
            "5AJFBZ", "VBFI1G", "TVH95P", "LVQWY4"]

count = 0
no_of_tests = len(correct)
for i in range(1, no_of_tests+1):
    a = cap(f"cap{i}.png")
    print(correct[i-1] == a, "\t", a, "\t", correct[i-1], "\n")
    count += 1 if correct[i-1] == a else 0
print("\nAccuracy: ", count/no_of_tests*100,"%")

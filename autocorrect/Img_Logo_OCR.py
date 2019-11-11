from PIL import Image
import pytesseract
import argparse
import cv2

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="Path to the image")
# args = vars(ap.parse_args())

# load the image and convert it to grayscale
# image = cv2.imread(args["image"])
import os

directory = '/home/uditshashankshukla/Desktop/Work/autocorrect-master/autocorrect/downloads/redbull logo'
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        image = cv2.imread(os.path.join(directory, filename))
        # cv2.imshow("Original", image)

        # Apply an "average" blur to the image

        blurred = cv2.blur(image, (3, 3))
        # cv2.imshow("Blurred_image", blurred)
        img = Image.fromarray(blurred)
        text = pytesseract.image_to_string(img, lang='eng')
        if text is not None and text != '':
            print(filename, "------>", text)
        else:
            print(filename)
        # cv2.waitKey(0)
        # print(os.path.join(directory, filename))
        continue
    else:
        continue

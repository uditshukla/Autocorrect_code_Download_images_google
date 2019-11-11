# image = cv2.imread(args["image"])
import os

import docx2txt
import openpyxl

directory = '/home/uditshashankshukla/Desktop/CMMi Search'
for filename in os.listdir(directory):
    if filename.endswith(".docx") or filename.endswith(".docx"):
        print('-------------------')
        print(filename)
        text = docx2txt.process(os.path.join(directory, filename))
        docx2txt
        print(text)
    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        print(filename)
        #wb = openpyxl.load_workbook(filename=os.path.join(directory, filename))
        #print(wb)

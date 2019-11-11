from xml.etree import cElementTree as ET

def extractText(filepath):
    with open(filepath, 'r') as file:
        data = file.read()
        # print(data)
    root = ET.fromstring(data)
    for page in list(root)[5]:
        content = page.find('text')
        return content.text.strip()
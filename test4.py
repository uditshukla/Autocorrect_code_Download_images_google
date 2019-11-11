import threading

from autocorrect.test import clean_dict

t4 = threading.Thread(target=clean_dict(300000, 400000))
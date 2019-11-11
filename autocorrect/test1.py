import threading

from autocorrect.test import clean_dict

t7 = threading.Thread(target=clean_dict(500000, 600000))
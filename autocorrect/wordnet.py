# import re
# import time
# import requests
#
# TAG_RE = re.compile(r'<[^>]+>')
#
#
# def remove_tags(text):
#     return TAG_RE.sub('', text)
#
#
# URL = "https://www.google.com/complete/search"
# headers = {
#     'cookie': 'NID=182=2fZqy7FgjgIZ8rwA1iPh6GxUXqa0I7ARNgQQzPkLID0ddOYxEg5E-m9kgdZsuiGOZ4zlY0DDpLsjzWkkhyKjN8jhikSUknCVeuI5U0tDR07juvgIJT9QRiWZDX4vyTvsJwOR4jm9UYYU-1ta--coCpVF91Za_NDSKPa6YVGrJE8; 1P_JAR=2019-04-25-04'}
#
#
# def get_google_autosuggest(q):
#     PARAMS = {'q': q, 'client': 'psy-ab'}
#     r = requests.get(url=URL, params=PARAMS, headers=headers)
#     time.sleep(2)
#     data = r.json()
#     length = len(data)
#     for i in range(length):
#         if i == 1:
#             response_list = data[i]
#             i_element_length = len(response_list)
#             for j in range(i_element_length):
#                 if j == 0:
#                     count = 0
#                     for item in response_list[j]:
#                         count += 1
#                         if count == 1:
#                             return remove_tags(str(item))
#
#         print(data[i])
# print(get_google_autosuggest('husbnd'))
import threading

from autocorrect.test import clean_dict

t7 = threading.Thread(target=clean_dict(600000, 700000))
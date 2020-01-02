# # This package will contain the spiders of your Scrapy project
# #
# # Please refer to the documentation for information on how to create and manage
# # your spiders.
#
import requests
from lxml import etree

r = requests.get("https://cd.esf.fang.com/chushou/3_210107166.htm",allow_redirects=False)
print(r.text)
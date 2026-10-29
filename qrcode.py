import pyqrcode
import png
from pyqrcode import QRCode

s="www.python3.hub.org"
url = pyqrcode.create(s)
pyqrcode.QRCode.show(url)
print(url)
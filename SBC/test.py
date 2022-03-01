import mimetypes,base64

s = '45.fd/468/'
print(s[0:-1])

fe = r'C:\SBC\SBCUsers\2290227486@qq.com\revie1.png'
fetype = mimetypes.guess_type(fe)
print(fetype[0].split('/')[0])

imgbase64data = "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="

with open('base64test.png','wb') as f:
    f.write(base64.b64decode(imgbase64data))

with open('base64test.png','rb') as f:
    # lsf = base64.b64decode(f.read())
    imgbase64 = "data:image/jpg;base64," + base64.b64encode(f.read()).decode()
print(imgbase64)

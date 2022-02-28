import mimetypes

s = '45.fd/468/'
print(s[0:-1])

fe = r'C:\SBC\SBCUsers\2290227486@qq.com\revie1.png'
fetype = mimetypes.guess_type(fe)
print(fetype[0].split('/')[0])
import zipfile
import os
import clipboard
import base64
import ctypes
import sys

class decryptor:
	def __init__(self,fn):
		self.fn=fn
	def __enter__(self):
		self.encrypt()
	def __exit__(self,t,v,b):
		open(self.fn,'wb').write(self.data0)
	def encrypt(self):
		dat=bytearray(open(self.fn,'rb').read())
		for n in range(len(dat)):
			dat[n]^=(n&255)
		open(self.fn,'wb').write(dat)

def pack():
	pth=os.getcwd()+'\\app package\\'

	fl=list(os.walk(pth))[0]

	zf=zipfile.ZipFile(pth+'tmp.zip','w')

	for x in fl[2]:
		zf.write(fl[0]+x,x)

	zf.close()

	encr=decryptor(pth+'tmp.zip')
	encr.encrypt()

	tgt=os.getcwd()+'\\dlls\\testabi.pyd'
	if os.path.isfile(tgt):
		os.remove(tgt)

	os.rename(pth+'tmp.zip',tgt)

	print('ok.')

def pic2code():
	fn=list(clipboard.cb2fn())[0]
	tp=fn[fn.rfind('.')+1:]
	s=base64.b64encode(open(fn,'rb').read())
	ans="\"data:image/%s;base64,%s\""%(tp,s.decode('utf-8'))
	clipboard.s2cb(ans)

def work():
	sel=input('1:pack\n2.pic to txt\n:')
	if sel=='2':
		pic2code()
	else:
		pack()


import apploader
import zipfile
import os
import clipboard
import base64
def pack():
	pth=os.getcwd()+'\\app package\\'

	fl=list(os.walk(pth))[0]

	zf=zipfile.ZipFile(pth+'tmp.zip','w')

	for x in fl[2]:
		zf.write(fl[0]+x,x)

	zf.close()

	encr=apploader.decryptor(pth+'tmp.zip')
	encr.encrypt()

	tgt=os.getcwd()+'\\dlls\\testabi.pyd'
	if os.path.isfile(tgt):
		os.remove(tgt)

	os.rename(pth+'tmp.zip',tgt)

	print('ok.')

def work():
	sel=input('1:pack\n2.pic to txt\n:')
	if sel=='2':
		fn=list(clipboard.cb2fn())[0]
		tp=fn[fn.rfind('.')+1:]
		s=base64.b64encode(open(fn,'rb').read())
		ans="\"data:image/%s;base64,%s\""%(tp,s.decode('utf-8'))
		clipboard.s2cb(ans)
	else:
		pack()


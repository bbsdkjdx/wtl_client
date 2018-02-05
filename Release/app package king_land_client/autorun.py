import __main__
import os
import arbinrpc
import win32tools
import binascii
import sys

# fixed code, do not change if possible.
#####################################################################################################################################
context_menu_js='''<script>document.oncontextmenu=function(){event.returnValue=event.srcElement.nodeName=='INPUT';}</script>'''

def _load_htmls(k):
	__main__.js.set_html(__main__.htmls[k].decode('utf-8')+context_menu_js)

def upgrade():
	return#todo
	fn='.\\dlls\\testabi.pyd'
	crc=binascii.crc32(open(fn,'rb').read())
	dat=cln.get_update(crc)
	if dat:
		open(fn,'wb').write(dat)
		__main__.msgbox('已更新软件版本，即将重新打开本软件！')
		win32tools.shell_execute(sys.argv[0],0,0)
		exit()

def on_html_ready():
	_load_htmls('0.html')
		
#####################################################################################################################################

cln=arbinrpc.Client('192.168.23.2',10000,1)

def f0_login(usr,pwd):
	if 1:#cln.login(usr,pwd): #todo
		_load_htmls('1.html')
	else:
		__main__.msgbox('密码错误！')

def f1_show_file(n):
	open('tmp.rar','wb').write(cln.get_file(n))
	win32tools.shell_execute('tmp.rar',0,0)


def f1_on_query(s):
	data= cln.search(s)
	return [x[2:]+x[1:2] for x in data]

import __main__
import os
import arbinrpc
import win32tools
import binascii
import sys
import ping

# fixed code, do not change if possible.
#####################################################################################################################################

#disable context menu and back.
extra_js='''<script>
document.oncontextmenu=function(){event.returnValue=event.srcElement.nodeName=='INPUT';};
document.onkeydown=function(){event.returnValue=!(event.keyCode==8 && event.srcElement.nodeName!='INPUT');}
</script>'''

def _load_htmls(k):
	__main__.js.set_html(__main__.htmls[k].decode('utf-8')+extra_js)

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
	__main__.exe.maindlg.set_timer(1000,1)
	__main__.exe.maindlg.set_hotkey(2,49,1)

def OnTimer():
	_id=__main__.stack['timer']

def OnHotkey():
	_id=__main__.stack['hotkey']
	__main__.js.alert(['hotkey'],_id)
#####################################################################################################################################

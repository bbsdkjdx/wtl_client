import __main__
import os
import arbinrpc
import win32tools
import binascii
import sys
import ctypes

# fixed code, do not change if possible.
#####################################################################################################################################
#disable contextmenu and backspace to goback.
extra_js='''<script>
document.oncontextmenu=function(){event.returnValue=event.srcElement.nodeName=='INPUT';};
document.onkeydown=function(){event.returnValue=!(event.keyCode==8 && event.srcElement.nodeName!='INPUT');}
</script>'''

def _show_menu(li,x=None, y=None):
	if x==None or y==None:
		pos = (ctypes.c_uint32*2)()
		ctypes.windll.user32.GetCursorPos(ctypes.byref(pos))
		x,y=pos
	menu = ctypes.windll.user32.CreatePopupMenu()
	for n in range(len(li)):
		ctypes.windll.user32.AppendMenuW(menu, 0x10, n+1, li[n])
	hwn = __main__.exe.maindlg.get_main_hwnd()
	ctypes.windll.user32.SetForegroundWindow(hwn)
	select = ctypes.windll.user32.TrackPopupMenuEx(menu, 0x1a3, x, y, hwn, 0)
	ctypes.windll.user32.DestroyMenu(menu)
	if select == 0:
		return ''
	return li[select-1]

def _load_htmls(k):
	__main__.js.set_html(__main__.htmls[k].decode('utf-8')+extra_js)

# the template of upgrade function.
def _upgrade():
	return#todo
	fn='.\\dlls\\testabi.pyd'
	crc=binascii.crc32(open(fn,'rb').read())
	dat=cln.get_update(crc)
	if dat:
		open(fn,'wb').write(dat)
		__main__.msgbox('已更新软件版本，即将重新打开本软件！')
		win32tools.shell_execute(sys.argv[0],0,0)
		exit()

_upgraded=False
def OnIdle():
	global _upgraded
	if not _upgraded:
		_upgrade()
		_upgraded=True

#called when the top html ready. Use as OnInitiaDialog().
def OnHtmlReady():
	_load_htmls('0.html')
	__main__.exe.maindlg.set_timer(1000,1)
	__main__.exe.maindlg.set_tray('ping.',1)
#	__main__.exe.maindlg.set_hotkey(2,49,1)

# define _on_timer() yourself below.
def OnTimer():
	_id=__main__.stack['timer']
	_on_timer(_id)

# define _on_hotkey() yourself below.
def OnHotkey():
	_id=__main__.stack['hotkey']
	_on_hotkey(_id)
	#__main__.js.alert(['hotkey'],_id)

# define _on_tray() yourself below.
# tp: 'l_down' 'l_dbclk' 'r_down' 'r_dbclk'
def OnTray(tp):
	_on_tray(tp)

allow_close=False
def OnClose():
	if allow_close:
		return 0
	__main__.exe.maindlg.show(0)
	return 1
#####################################################################################################################################

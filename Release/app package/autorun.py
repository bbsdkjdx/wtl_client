import __main__
import os
import arbinrpc
import win32tools
import binascii
import sys
import ctypes

# fixed code, do not change if possible.
#####################################################################################################################################

#app will allow only one instance if mutex_token is specified.
mutex_token="hc_xxzd"

#if tray_txt not None,show tray,and only can closed by tray.
tray_txt='环翠国土信息平台'

#set to html's <base> tag.
_html_base=os.getcwd()+'\\dlls\\'

#disable contextmenu and backspace to goback.
extra_js='''<!doctype html><base href="%s" /><script>
document.oncontextmenu=function(){event.returnValue=event.srcElement.nodeName=='INPUT';};
document.onkeydown=function(){event.returnValue=!(event.keyCode==8 && event.srcElement.nodeName!='INPUT');}
</script>''' % (_html_base)

#switch pages
def _load_htmls(k):
	s_html=__main__.htmls[k].decode('utf-8').strip()
	__main__.js.set_html(extra_js+s_html)

#menu support
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

#set autorun in registry,specify item name by 'name',set if enable else delete.
def _set_autorun(name,enable):
	import win32api,win32con,sys,os
	mk=win32con.HKEY_LOCAL_MACHINE
	sk='SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
	fn=sys.argv[0]
	if '\\' not in fn:
		fn=os.getcwd()+'\\'+fn
	k=win32api.RegOpenKey(mk,sk,0,win32con.KEY_ALL_ACCESS)
	if enable:
		win32api.RegSetValueEx(k,name,0,win32con.REG_SZ,fn)
	else:
		win32api.RegDeleteValue(k,name)

#called when the top html ready. Use as OnInitiaDialog().
def OnHtmlReady():
	#_load_htmls('0.html')#call twice to make focus() work normal.
	_load_htmls('main.html')
#	__main__.exe.maindlg.set_timer(1000,1)
	if tray_txt:
		__main__.exe.maindlg.set_tray(tray_txt,1)
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

allow_close= not tray_txt
def OnClose():
	if allow_close:#close directly if no tray.
		return 0
	else:#hide main window.
		__main__.exe.maindlg.show(0)
		return 1


#####################################################################################################################################

class CEverythig(object):
	pass

usr_info=CEverythig()
usr_info.usr='未登录'
usr_info.pwd=''

def _on_tray(tp):
	global allow_close
	if tp=='l_dbclk':
		__main__.exe.maindlg.show(1)
	if tp=='r_down':
		sel = _show_menu(['主窗口', '退出'])
		if sel=='退出':
			allow_close=True
			__main__.exe.maindlg.close_wnd()
		if sel=='主窗口':
			__main__.exe.maindlg.show(1)

def main_login():
	_load_htmls('login.html')

def main_get_user_info():
	return '当前用户：%s'%(usr_info.usr)

def login_get_user_pwd():
	return usr_info.usr,usr_info.pwd

def login_login(usr,pwd):
	#check usr,pwd
	usr_info.usr=usr
	usr_info.pwd=pwd
	usr_info.token=usr
	_load_htmls('main.html')

def login_back():
	_load_htmls('main.html')

def close_wnd():
	__main__.exe.maindlg.close_wnd()
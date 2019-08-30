import __main__
import os
import arbinrpc
import win32tools
import binascii
import sys
import ctypes
import base64
import socket

import login
__main__.login=login

import todo
__main__.todo=todo

import inputer
__main__.inputer=inputer

import kingland
__main__.kingland=kingland

import query_db
__main__.query_db=query_db

import little_program
__main__.little_program=little_program

import html_control
__main__.html_control=html_control

socket.setdefaulttimeout(1)
#####################################################################################################################################
# fixed code, do not change if possible.

#set to html's <base> tag.
_html_base=os.getcwd()+'\\dlls\\'

#disable contextmenu and backspace to goback.
extra_js='''<!doctype html><base href="%s" /><script>
document.oncontextmenu=function(){event.returnValue=event.srcElement.nodeName=='INPUT'||event.srcElement.nodeName=='TEXTAREA';};
document.onkeydown=function()
{
	if(event.keyCode==8 && event.srcElement.nodeName!='INPUT' && event.srcElement.nodeName!='TEXTAREA')
	{
		event.returnValue=false;
		return;
	}
}
PyFun=window.parent.ExtFun
</script>''' % (_html_base)

#load page.
def _load_htmls(k,async=True):
	htmls=__main__.htmls[k].decode('utf-8').strip()
	__main__.js.set_html(extra_js+htmls,async)

#menu support
def _show_menu(li,x=None, y=None):
	if x==None or y==None:
		pos = (ctypes.c_uint32*2)()
		ctypes.windll.user32.GetCursorPos(ctypes.byref(pos))
		x,y=pos
	menu = ctypes.windll.user32.CreatePopupMenu()
	for n in range(len(li)):
		ctypes.windll.user32.AppendMenuW(menu, 0x10, n+1, li[n])
	hwn = __main__.exe.get_main_hwnd()
	ctypes.windll.user32.SetForegroundWindow(hwn)
	select = ctypes.windll.user32.TrackPopupMenuEx(menu, 0x1a3, x, y, hwn, 0)
	ctypes.windll.user32.DestroyMenu(menu)
	if select == 0:
		return ''
	return li[select-1]

# the template of upgrade function.
def update():
	dic=cln.get_update_datas(None)
	needs=[]
	if not dic:
		return False
	for f in dic:
		try:
			dat=open('.'+f,'rb').read()
		except:
			dat=b''
		crc=binascii.crc32(dat)
		if crc!=dic[f]:
			needs.append(f)

	if '\\upgrade.exe' not in needs:
		dat=open(sys.argv[0],'rb').read()
		crc=binascii.crc32(dat)
		if crc!=dic['\\upgrade.exe']:
			needs.append('\\upgrade.exe')

	if not needs:
		return False
	dic=cln.get_update_datas(needs)
	for f in dic:
		open('.'+f,'wb').write(dic[f])
	fn_updater=sys.argv[0]
	pos=fn_updater.rfind('\\')
	fn_updater=fn_updater[:pos+1]+'upgrade.exe'
	ctypes.windll.shell32.ShellExecuteW(0,'open',fn_updater,str(os.getpid()),0,1)
	return True

 
#set autorun in registry,specify item name by 'name',set if enable else delete.
def _set_autorun(name,enable=True,para=''):
	import win32api,win32con,sys,os
	mk=win32con.HKEY_LOCAL_MACHINE
	sk='SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
	fn=sys.argv[0]
	if '\\' not in fn:
		fn=os.getcwd()+'\\'+fn
	if para:
		fn+=' '+para
	k=win32api.RegOpenKey(mk,sk,0,win32con.KEY_ALL_ACCESS)
	if enable:
		win32api.RegSetValueEx(k,name,0,win32con.REG_SZ,fn)
	else:
		win32api.RegDeleteValue(k,name)

#####################################################################################	

#app will allow only one instance if mutex_token is specified.
mutex_token="hc_xxzd"

#if tray_txt not None,show tray,and only can closed by tray.
#tray_txt=''
tray_txt='环翠国土信息平台'

#determine if show alarms.
need_alarm=False

#try to do as upgrade helper at the beginging of app start.

def quit_if_not_first_instance():
	ctypes.windll.kernel32.CreateMutexW(0,0,tray_txt)
	if ctypes.windll.kernel32.GetLastError()==183:
		ctypes.windll.kernel32.ExitProcess(0)

def try_as_upgrade_helper():
	try:
		#__main__.msgbox(sys.argv)
		pid=int(sys.argv[-1])
		fn=win32tools.pid2fn(pid)
		win32tools.killpid(pid)
		__main__.msgbox('平台客户端有新版本，即将重新打开！')
		ctypes.windll.kernel32.CopyFileW(sys.argv[0],fn,0)
		ctypes.windll.shell32.ShellExecuteW(0,'open',fn,0,0,1)
		ctypes.windll.kernel32.ExitProcess(0)
	except:
		pass

def clear_dead_tray():
    import ctypes
    FindWindowW=ctypes.windll.user32.FindWindowW
    FindWindowExW=ctypes.windll.user32.FindWindowExW
    w1=FindWindowW('Shell_TrayWnd',0)
    w2=FindWindowExW(w1,0,'TrayNotifyWnd',0)
    w3=FindWindowExW(w2,0,'SysPager',0)
    w4=FindWindowExW(w3,0,'ToolbarWindow32',0)
    rect=(ctypes.c_uint32*4)()
    ctypes.windll.user32.GetWindowRect(w4,ctypes.byref(rect))
    wid=rect[2]-rect[0]
    for x in range(0,wid,20):
        ctypes.windll.user32.PostMessageW(w4,0x200,0,5<<16|x)

def kill_pre_instances():
	pid_me=win32tools.get_my_pid()
	fn_me=win32tools.pid2fn(pid_me)
	for pid in win32tools.get_pids():
		if pid!=pid_me and win32tools.pid2fn(pid)==fn_me:
			win32tools.killpid(pid)
			clear_dead_tray()

#called when the frame html ready. Use as OnInitiaDialog().
def OnInitApp():
	try_as_upgrade_helper()
	kill_pre_instances()
	#quit_if_not_first_instance()
	__main__.exe.set_tray(tray_txt,0)

	try:
		if update():
			__main__.exe.set_tray(tray_txt,-1)#delete tray
			return
	except:
		__main__.msgbox('无法连接服务器，进入离线模式。','环翠国土信息平台')
		#__main__.exe.set_tray(tray_txt,-1)
		#ctypes.windll.kernel32.ExitProcess(0)
		
	_load_htmls('theapp.html')
	_set_autorun('hcgt_xxpt',True,'auto')
	__main__.exe.set_timer(600,1)#tray ico flash.
	__main__.exe.set_timer(60000,1)#check if need alarm.
	
	#check alarm on start.

		#__main__.msgbox('hide')
#	__main__.exe.set_hotkey(2,49,1)

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
		__main__.exe.show(0)
		return 1



#####################################################################################################################################
cln=arbinrpc.Client('10.176.132.252',10001)



def _on_tray(tp):
	global allow_close
	if tp=='l_dbclk':
		__main__.exe.show(1)
	if tp=='r_down':
		sel = _show_menu(['主窗口', '退出'])
		if sel=='退出':
			allow_close=True
			__main__.exe.close_wnd()
		if sel=='主窗口':
			_load_htmls('theapp.html')

def main_login():
	_load_htmls('login.html')

def close_wnd():
	__main__.exe.close_wnd()

tray_flg=True
def _on_timer(_id):
	global tray_flg
	if _id==600:
		if need_alarm and tray_flg:
			__main__.exe.set_tray(tray_txt,2)
		else:
			__main__.exe.set_tray(tray_txt,1)
		tray_flg=not tray_flg
		return
	if _id==60000:
		flush_alarm()

def flush_alarm():
	global need_alarm
	need_alarm=todo.have_emergency_todos()

def go_home_page():
	_load_htmls('theapp.html')

first_show=True
def hide_if_autorun():
	global first_show
	if 'auto' in sys.argv and first_show:
		first_show=False
		__main__.exe.show(0)


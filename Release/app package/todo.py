import __main__
import theapp
import login
import time
import datetime
import os
def on_todo():
	theapp._load_htmls('todo.html')

events=[]
last_date_time=0
def update_events():
	global events,last_date_time
	a,b=theapp.cln.get_events(login.log_info.usr,last_date_time)
	if a!=last_date_time:
		last_date_time=a
		events=b
#[ [1, 'aa', 'bbb', '2018-05-09','重要'], [['毕彬', '毕彬', 1525850204.614087, '创建本事件','附件名']] ],
def translate_event(evt):
	stas=evt[1]
	ret1=''
	for n,sta in enumerate(stas):
		t=time.localtime(sta[2])
		st='%d-%d-%d %d:%d:%d'%(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
		s_on_clk="PyFun('todo.show_accessory','%d.%d.%s')"%(evt[0][0],n,sta[4])
		ret1+='[%s] %s->%s %s'%(st,sta[0],sta[1],sta[3])
		if sta[4]:
			ret1+='<font onclick="'+s_on_clk+'" onmouseout="mouseout(this)" onmouseover="mousein(this)" style="cursor:pointer;color:blue">&nbsp&nbsp&nbsp&nbsp附件：'\
			+sta[4]+'</font><br>'
		else:
			ret1+='<br>'
	while 1:
		if stas[-1][1] in [login.log_info.usr,login.log_info.office]:
			ret2='待办'
			break
		if stas[-1][1]=='办结':
			ret2='办结'
			break
		ret2='已处理'
		break
	return [ret1,ret2]

def get_sort_key(evt_ex):
	k1= ['待办','已处理','办结'].index(evt_ex[3])
	k2=['重要','普通','不重要'].index(evt_ex[0][4])
	try:
		k3=-int(evt_ex[0][3].replace('-',''))
	except:
		k3=0
	return k1,k2,k3

def get_events(event_type):
	update_events()
	events_ex=sorted((x+translate_event(x) for x in events),key=get_sort_key)
	if event_type=='全部':
		return events_ex
	return [x for x in events_ex if x[3]==event_type]

def num2date(n):
	td=datetime.date.today()
	dlt=datetime.timedelta(n)
	td+=dlt
	return str(td)

def have_emergency_todos():
	update_events()
	evts=[x+translate_event(x) for x in events]
	td=datetime.date.today()
	dlt=datetime.timedelta(1)
	s=num2date(1)
	for evt in evts:
		if evt[3]=='待办' and evt[0][3]<s:
			return True
	return False


def get_n_todo():
	try:
		return len(get_events('待办'))
	except:
		return 0

def get_users_data(usr):
	try:
		return ['办结']+theapp.cln.get_user_combo_data(usr)
	except:
		return []

def get_dates():
	return theapp.cln.get_dates()

def on_create_event(title,describe,deadline,priority,fn,to_):
	fn_s,dat='',b''
	if fn:
		dat=open(fn,'rb').read()
		fn_s=fn[fn.rfind('\\')+1:]
	theapp.cln.on_create_event(login.log_info.usr,to_,title,describe,deadline,priority,fn_s,dat)

def on_modify_event(_id,title,describe,deadline,priority):
	theapp.cln.on_modify_event(_id,title,describe,deadline,priority)

def on_delete_event(_id):
	theapp.cln.on_delete_event(_id)

def on_handle_event(_id,comment,_to,fn):
	fn_s,dat='',b''
	if fn:
		dat=open(fn,'rb').read()
		fn_s=fn[fn.rfind('\\')+1:]
	theapp.cln.on_handle_event(_id,login.log_info.usr,comment,_to,fn_s,dat)

def on_recall_status(_id):
	theapp.cln.on_recall_status(_id)

def show_accessory(fn):
	import win32tools
	dat=theapp.cln.get_accessory(fn)
	#ext=fn[fn.rfind('.'):]
	pth='c:\\hcgt_temp\\'
	if not os.path.isdir(pth):
		os.mkdir(pth)
	open(pth+fn,'wb').write(dat)
	win32tools.shell_execute(pth+fn,show=0,block=0)

def confirm(s):
	import ctypes
	wnd=ctypes.windll.user32.GetForegroundWindow()
	return True if 6==ctypes.windll.user32.MessageBoxW(wnd,str(s),'',0x34) else False
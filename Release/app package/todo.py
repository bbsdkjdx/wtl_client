import __main__
import theapp
import login
import time
def on_todo():
	theapp._load_htmls('todo.html')

events=[]
#[[1, 'aa', 'bbb', '2018-05-09', [['毕彬', '毕彬', 1525850204.614087, '创建本事件']]]]
def translate_status(stas):
	ret1=''
	for sta in stas:
		t=time.localtime(sta[2])
		st='%d-%d-%d %d:%d:%d'%(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
		ret1+='[%s] %s->%s %s'%(st,sta[0],sta[1],sta[3]) +'<br>'
	ret2='未处理' if stas[-1][1]==login.log_info.usr else '已处理'
	return [ret1,ret2]

def get_events(event_type):
	global events
	events=theapp.cln.get_events(login.log_info.usr)
	events=[x+translate_status(x[4]) for x in events]
	if event_type=='待办':
		return [x for x in events if x[4][-1][1]==login.log_info.usr]
	if event_type=='已完成':
		return [x for x in events if x[4][-1][1]!=login.log_info.usr]
	if event_type=='全部':
		return events
	return []			
	
def get_users_data():
	try:
		return ['办结']+theapp.cln.get_user_combo_data()
	except:
		return []

def get_dates():
	return theapp.cln.get_dates()

def on_create_event(title,describe,deadline):
	theapp.cln.on_create_event(login.log_info.usr,title,describe,deadline)

def on_modify_event(_id,title,describe,deadline):
	theapp.cln.on_modify_event(_id,title,describe,deadline)


def on_handle_event(_id,comment,_to):
	theapp.cln.on_handle_event(_id,login.log_info.usr,comment,_to)

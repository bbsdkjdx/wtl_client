import pickle
import re
import arbinrpc
import binascii
import datetime
import time
import os
from collections import OrderedDict
from .datastructure import RealTimeDiskDict
#constants
PORT=10001
FILE_USERS=__path__[0]+'\\users.p'
FILE_EVENTS=__path__[0]+'\\events.dat'
FILE_UPGRADE=__path__[0]+'\\testabi.pyd'

#load users
try:
	users=pickle.load(open(FILE_USERS,'rb'))
except:
	users=OrderedDict()

#events
events=RealTimeDiskDict(FILE_EVENTS)

#declare server.
svr=arbinrpc.Server('0.0.0.0',PORT,5)

def save_users():
	pickle.dump(users,open(FILE_USERS,'wb'))

#define decorator
def reg_svr(fun):
	svr.reg_fun(fun)
	return fun

def my_walk(rt):
	for d in os.walk(rt):
		for f in d[2]:
			yield d[0]+'\\'+f

def get_update_dict():
	pth=__path__[0]+'\\updates'
	L=len(pth)
	ret=dict()
	for f in my_walk(pth):
		dat=open(f,'rb').read()
		crc=binascii.crc32(dat)
		ret[f[L:]]=[crc,dat]
	return ret

update_dict=get_update_dict()

#old version compatible.no use in new version.
@reg_svr
def get_update(cln_crc):
	try:
		update_data=open(FILE_UPGRADE,'rb').read()
	except:
		update_data=b''
	crc32=binascii.crc32(update_data)
	if crc32==cln_crc:
		return b''
	return update_data

#new version update,return all files needed update.
@reg_svr
def get_update_datas(file_list=None):
	if file_list is None:#return crc32 dict to client
		return { x:update_dict[x][0] for x in update_dict}
	else:#return file data acroding file_list
		return { x:update_dict[x][1] for x in file_list}

@reg_svr
def modify_password(usr,pwd):
	if usr in users:
		users[usr][0]=pwd
		save_users()
		return True
	return False

@reg_svr
def login(usr,pwd):
	if usr not in users:
		return False
	_pwd,_ke=users[usr]
	if _pwd==pwd:
		return usr,_ke
	return False

@reg_svr
def get_user_combo_data(usr):
	_ofc=''
	my_ofc=users[usr][1]
	ret=[]
	ret_self=['__当前科室__ ']
	for x in users:
		ofc=users[x][1]
		if ofc==my_ofc:
			ret_self.append(x)
			continue
		if ofc!=_ofc:
			_ofc=ofc
			ret.append('___'+ofc+'___ ')
		ret.append(x)
	return ret_self+ret

@reg_svr
def get_dates():#get 62 days from now on.
	td=datetime.date.today()
	delt=datetime.timedelta(1)
	ret=[]
	for x in range(62):
		ret.append(str(td))
		td+=delt
	return ret

@reg_svr
def on_create_event(usr,tp,describe,deadline,priority='普通'):
	_id=len(events)+1
	_status=[usr,usr,time.time(),'创建事件']#status [from,to,time,comment]
	_evt=[[_id,tp,describe,deadline,priority],[_status]]
	events[_id]=_evt
# events over view
#[
#[ [1, 'aa', 'bbb', '2018-05-09','重要'], [['毕彬', '毕彬', 1525850204.614087, '创建本事件']] ],
#]
@reg_svr
def on_handle_event(_id,usr,cmnt,_to):
	if _id in events:
		evt=events[_id]
		sta=[usr,_to,time.time(),cmnt]
		evt[1].append(sta)
		events[_id]=evt
		
@reg_svr
def on_modify_event(_id,title,describe,deadline,priority='普通'):
	if _id in events:
		evt=events[_id]
		evt[0][1]=title
		evt[0][2]=describe
		evt[0][3]=deadline
		evt[0][4]=priority
		events[_id]=evt
			
#old version compatible.no use in new version.
@reg_svr
def get_events(usr):
	ret=[]
	for _id in events:
		evt=events[_id]
		for sta in evt[1]:
			if sta[1]==usr:
				ret.append(evt)
				break
	ret2=[]
	for x in ret:
		y=x[0][:-1]
		y.append(x[1])
		ret2.append(y)
	return ret2

@reg_svr
def get_events2(usr):
	ret=[]
	for _id in events:
		evt=events[_id]
		for sta in evt[1]:
			if sta[1]==usr:
				ret.append(evt)
				break
	return ret

svr.start()
import __main__
import os
import arbinrpc
import win32tools
import binascii
import sys
import ctypes
import base64
import pickle
import theapp
def encode(s):
	return base64.b64encode(s.encode('utf-8'))

def decode(s):
	return base64.b64decode(s).decode('utf-8')

class CEverythig(object):
	pass

log_info=CEverythig()
log_info.usr=''
log_info.pwd=''
log_info.office=''
log_info.token=''

def load_cache():
	try:
		dat=pickle.load(open('loin_cache.p','rb'))
		log_info.usr=decode(dat[0])
		log_info.pwd=decode(dat[1])
	except:
		pass

load_cache()

def save_cache():
	dat=[encode(log_info.usr),encode(log_info.pwd)]
	pickle.dump(dat,open('loin_cache.p','wb'))


def get_user_info():
	return log_info.usr,log_info.office

def get_user_pwd():
	return log_info.usr,log_info.pwd

def _login():
	import theapp
	ret=theapp.cln.login(log_info.usr,log_info.pwd)
	if ret:
		log_info.office=ret[1]
		log_info.token=log_info.usr
		save_cache()
		return True	
	else:
		log_info.usr=''
		log_info.pwd=''
		log_info.office=''
		log_info.token=''
		save_cache()
		return False


def on_login(usr,pwd):
	log_info.usr=usr
	log_info.pwd=pwd
	if _login():
		theapp.go_home_page()
	else:
		__main__.msgbox('请检查用户名和密码!')

	
def do_login(show=False):
	if not show:
		load_cache()
		_login()
	else:
		theapp._load_htmls('login.html')

def modify_password(pwd):
	if log_info.usr=='':
		__main__.msgbox('请先登录！','密码修改失败')
		return
	if pwd[0]!=log_info.pwd:
		__main__.msgbox('原密码不正确。','密码修改失败')
		return
	if pwd[1]!=pwd[2]:
		__main__.msgbox('两次输入的新密码不一至。','密码修改失败')
		return
	if theapp.cln.modify_password(log_info.usr,pwd[1]):
		log_info.pwd=pwd[1]
		save_cache()
		__main__.msgbox('密码修改成功！','密码修改')
	else:
		__main__.msgbox('用户名不正确！','密码修改失败')
	
    #        u_p=window.parent.ExtFun('login.get_user_pwd');
     #       if(u_p[0]==''){window.parent.ExtFun('msgbox','请先登录！','密码修改失败');return;}
     #       if(p[0]!=u_p[1]){window.parent.ExtFun('msgbox','原密码不正确。','密码修改失败');return;}
     #       if(p[2]!=p[1]){window.parent.ExtFun('msgbox','两次输入的新密码不一至。','密码修改失败');return;}




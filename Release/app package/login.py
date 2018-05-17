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
	
	




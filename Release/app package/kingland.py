import __main__
import theapp
import login
import time
import os
import arbinrpc
import win32tools
import binascii
import sys

def show_page():
	theapp._load_htmls('kingland.html')

def show_file(n):
	usr=login.log_info.usr
	tm=time.ctime()
	open('tmp.rar','wb').write(theapp.cln.kingland_file(usr,tm,n))
	win32tools.shell_execute('tmp.rar',0,0)


def on_query(s):
	usr=login.log_info.usr
	tm=time.ctime()
	data= theapp.cln.kingland_search(usr,tm,s)
	return [x[2:]+x[1:2] for x in data]

n=0
def fun(s):
	global n
	__main__.exe.set_title(s+str(n))
	n+=1
	return [n]+['a']*n
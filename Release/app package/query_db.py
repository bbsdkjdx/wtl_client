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
	theapp._load_htmls('query_db.html')

def show_file(db_type,n):
	usr=login.log_info.usr
	tm=time.ctime()

	open('tmp.rar','wb').write(theapp.cln.db_file(usr,tm,db_type,n))
	win32tools.shell_execute('tmp.rar',0,0)


def on_query(db_type,s):
	usr=login.log_info.usr
	tm=time.ctime()
	data= theapp.cln.db_search(usr,tm,db_type,s)
	return data

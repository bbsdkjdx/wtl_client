import __main__
import os
import arbinrpc
import win32tools
import binascii
import sys
import ping

# fixed code, do not change if possible.
#####################################################################################################################################
extra_js='''<script>
document.oncontextmenu=function(){event.returnValue=event.srcElement.nodeName=='INPUT';};
document.onkeydown=function(){event.returnValue=!(event.keyCode==8 && event.srcElement.nodeName!='INPUT');}
</script>'''

def _load_htmls(k):
	__main__.js.set_html(__main__.htmls[k].decode('utf-8')+extra_js)

def upgrade():
	return#todo
	fn='.\\dlls\\testabi.pyd'
	crc=binascii.crc32(open(fn,'rb').read())
	dat=cln.get_update(crc)
	if dat:
		open(fn,'wb').write(dat)
		__main__.msgbox('已更新软件版本，即将重新打开本软件！')
		win32tools.shell_execute(sys.argv[0],0,0)
		exit()

def on_html_ready():
	_load_htmls('0.html')
	__main__.exe.maindlg.set_timer(1000,1)
	__main__.exe.maindlg.set_hotkey(2,49,1)

def OnTimer():
	_id=__main__.stack['timer']
	_on_timer(_id)

def OnHotkey():
	_id=__main__.stack['hotkey']
	__main__.js.alert(['hotkey'],_id)
#####################################################################################################################################

#load settings.
import pickle
try:
	names=pickle.load(open('ip.p','rb'))
except:
	names=[['','',0,0] for x in range(8)]
cur_set=0

#ping handler
def on_ping_echo(para):
	tm=para[1]
	if tm>1:
		tm=1
	for x in names:
		if x[1]==para[0]:
			x[2]=tm
pn=ping.CPing(8,on_ping_echo,0,0)

#beep routine
from winsound import Beep
import time
import threading
need_beep=0
def beep_loop():
	global need_beep
	while 1:
		if need_beep:
			Beep(3000,1000)
		else:
			time.sleep(1)
thd_beep=threading.Thread(target=beep_loop)
thd_beep.start()

def prepare_value(nm,ip,tm,alm):
	global need_beep
	width=int((1-tm)*100)
	p_color='#f80303'
	if(width>25):p_color='#f87103'
	if(width>50):p_color='#f8f403'
	if(width>75):p_color='#17f803'
	width='%d%%'%(width)

	alm_con='无'
	if alm==1:alm_con='断网'
	if alm==-1:alm_con='联网'
	txt='%s [%s] 警报条件：%s 响应时间：%f' %(nm,ip,alm_con,tm)
	t_color='#000000'
	if ( (tm==1 and alm==1) or (tm<1 and alm==-1) ):
		t_color='#f80303'
		need_beep=1
	return [width,p_color,txt,t_color]



def _on_timer(_id):
	global need_beep
	need_beep=0
	vls=[ prepare_value(*x) for x in names]
	#__main__.msgbox(vls)
	__main__.js.ifrf.setvalue(vls)
	for x in names:
		x[2]=1
		if x[1]:
			pn.send_ping(x[1])
	
 
def f0_ping(ip):
	__main__.js.ifrf.show('no result')
	pn.send_ping(ip)

def f0_set_name_ip(x):
	global cur_set
	cur_set=x
	_load_htmls('1.html')

def f1_set_name_ip(nm,ip,cond):
	if nm!=0:
		name=names[cur_set]
		name[0]=nm
		name[1]=ip
		name[3]=int(cond)
	_load_htmls('0.html')
	pickle.dump(names,open('ip.p','wb'))

def f1_get_name_ip():
	return names[cur_set]
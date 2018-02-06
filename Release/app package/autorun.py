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

names=[['','',0] for x in range(8)]
cur_set=0

def on_ping_echo(para):
	tm=para[1]
	if tm>1:
		tm=1
	for x in names:
		if x[1]==para[0]:
			x[2]=tm

pn=ping.CPing(8,on_ping_echo,0,0)

def _on_timer(_id):
	__main__.js.ifrf.setvalue(*[1-x[2] for x in names])
	for x in names:
		x[2]=1
		if x[1]:
			pn.send_ping(x[1])
	

def f0_ping(ip):
	__main__.js.ifrf.show('no result')
	pn.send_ping(ip)

def f0_get_name_ip():
	return [ '{0}  [{1}]  响应时间:{2}'.format(*x) for x in names]

def f0_get_values():
	return [x[2] for x in names]

def f0_set_name_ip(x):
	global cur_set
	cur_set=x
	_load_htmls('1.html')

def f1_set_name_ip(nm,ip):
	if nm!=0:
		name=names[cur_set]
		name[0]=nm
		name[1]=ip
	_load_htmls('0.html')

def f1_get_name_ip():
	return names[cur_set]
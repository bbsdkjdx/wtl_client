import __main__
import theapp
	
def do_input(title,items,s_callback,checker=[]):
	"""do_input(title,items,s_callback);
	example: window.parent.ExtFun('inputer.do_input','输入标题',[],'input_complete')
	"""
	__main__.js.new_ifr()
	theapp._load_htmls('inputer.html',async=0)
	__main__.js.ifrf.on_init(title,items,s_callback)
	push_checker(checker)

check_list=[]

def push_checker(checker):
	check_list.append(checker)

def pop_checker():
	if check_list:
		check_list.pop()

def check_ok(p):#check_item use "p[x]" refer data.
	for s_eval,msg in check_list[-1]:
		if eval(s_eval):
			__main__.msgbox(msg,'输入有误')
			return False
	return True

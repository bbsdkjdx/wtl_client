import __main__
import theapp
	
def do_input(title,items,s_callback):
	"""do_input(title,items,s_callback);
	example: window.parent.ExtFun('inputer.do_input','输入标题',[],'input_complete')
	"""
	__main__.js.switch_ifr()
	theapp._load_htmls('inputer.html',async=0)
	__main__.js.ifrf.on_init(title,items,s_callback)
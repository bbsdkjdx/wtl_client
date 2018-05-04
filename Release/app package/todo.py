import __main__
import theapp

def on_todo():
	theapp._load_htmls('todo.html')

def get_data(event_type):
	if event_type=='待办':
		return [[1,2,3,4]]*50
	if event_type=='已完成':
		return [[5,6,7,8]]*50
	if event_type=='全部':
		return [[1,2,3,4]]*50+[[5,6,7,8]]*50
	return []			
	
def get_combo_data():
	try:
		return theapp.cln.get_user_combo_data()
	except:
		return []


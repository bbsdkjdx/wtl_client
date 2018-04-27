import __main__
import theapp

def on_todo():
	theapp._load_htmls('todo.html')

def get_data(event_type):
	if event_type=='待办':
		return [[1,2,3,4]]*5
	if event_type=='已完成':
		return [[5,6,7,8]]*5
	if event_type=='全部':
		return [[1,2,3,4]]*5+[[5,6,7,8]]*5
	return []			
	




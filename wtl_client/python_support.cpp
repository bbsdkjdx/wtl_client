#include "stdafx.h"
#include "python_support.h"


PyObject  *pRet = nullptr;
PyObject  *pModule = nullptr;



char *pre_code =
"import traceback as _traceback\n"
"import ctypes as _ctypes\n"
"import json as _json\n"
"from threading import get_ident as _get_thd_id\n"

//stack to transform parameters between exe and python.
"stack=dict()\n"

//show message box before foreground window.
"def msgbox(s,title=''):\n"
" _ctypes.windll.user32.MessageBoxW(_ctypes.windll.user32.GetForegroundWindow(),str(s),title,0x40)\n"

//define exe funciton management class,exe is the object,type it can see all functions.
"class CAnything(object):\n"
"    def __repr__(self):\n"
"        dic=self.__dict__\n"
"        return '\\n**************************************************\\n'.join((x+'\\n'+dic[x].__dict__.get('__doc__','') for x in dic))\n"
"exe=CAnything()\n"
"def _build_exe_fun__(mod,fnn, fmt, adr,doc):\n"
"    dic = {'#': '_ctypes.c_void_p', \n"
"           's':'_ctypes.c_char_p','S': '_ctypes.c_wchar_p',\n"
"           'l': '_ctypes.c_int32', 'u': '_ctypes.c_uint32',\n"
"           'L': '_ctypes.c_int64', 'U': '_ctypes.c_uint64',\n"
"           'f': '_ctypes.c_float', 'F': '_ctypes.c_double'}\n"
"    cmd = '_ctypes.CFUNCTYPE('\n"
"    cmd += ','.join(map(lambda x: dic[x], fmt))\n"
"    cmd += ')('+str(adr)+')'\n"
"    if not mod:\n"
"        exe.__dict__[fnn]=eval(cmd)\n"
"        exe.__dict__[fnn].__doc__=doc\n"
"        return\n"
"    if mod not in exe.__dict__:exe.__dict__[mod]=CAnything()\n"
"    exe.__dict__[mod].__dict__[fnn] = eval(cmd)\n"
"    exe.__dict__[mod].__dict__[fnn].__doc__=doc\n"



"_thd_dict=dict()\n"
//two caller in html to call back and forth.
"def _get_caller():\n"
"    import htmldoc\n"
"    wnd=exe.maindlg.get_browser_hwnd()\n"
"    doc=htmldoc.wnd2htmldoc(wnd)\n"
"    dic=dict()\n"
"    dic['_exe_caller']=doc.getElementById('execaller')\n"
"    dic['_js_caller']=doc.getElementById('jscaller')\n"
"    _thd_dict[_get_thd_id()]=dic\n"

//treate js call exe,
"def _ext_fun():\n"
"    if _get_thd_id() not in _thd_dict:\n"
"        _get_caller()\n"
"    _exe_caller=_thd_dict[_get_thd_id()]['_exe_caller']\n"
"    fun,*para=_json.loads(_exe_caller.value)\n"
"    try:\n"
"        fun=eval(fun)\n"
"        _exe_caller.value= _json.dumps(fun(*para))\n"
"    except Exception as exp:\n"
"        _exe_caller.value= _json.dumps(str(exp))\n"


//treat exe call js.
"def _call_js(fun_name,paras):\n"
"    s1=_json.dumps([fun_name,paras])\n"
"    if _get_thd_id() not in _thd_dict:\n"
"        _get_caller()\n"
"    _js_caller=_thd_dict[_get_thd_id()]['_js_caller']\n"
"    _js_caller.value=s1\n"
"    _js_caller.click()\n"
"    s2=_js_caller.value\n"
"    return _json.loads(s2)\n"
//the wrapper of exe call js.
"class CJs(object):\n"
"    def __init__(self, name = None):\n"
"        self.name = name if name else[]\n"
"    def __getattr__(self, name):\n"
"        return CJs(self.name + [name])\n"
"    def __call__(self, *args):\n"
"        return _call_js('.'.join(self.name),args)\n"
"js=CJs()\n"

;


void _init_python()//call it before use other function else.
{
	Py_Initialize(); 
	PyEval_InitThreads();
	Py_SetProgramName(_T(""));  /* optional but recommended */ //define APP_NAME first.
	//makes sys.argv availiable.
	LPTSTR cmd = ::GetCommandLine();
	int argc = 0;
	LPWSTR* argv = ::CommandLineToArgvW(cmd, &argc);
	PySys_SetArgv(argc, argv);
	PyRun_SimpleString(pre_code);
	//set current directory.
	wchar_t szExeFilePathFileName[MAX_PATH];
	GetModuleFileName(NULL, szExeFilePathFileName, MAX_PATH);
	int x;
	for (x = wcslen(szExeFilePathFileName); szExeFilePathFileName[x] != '\\'; --x);
	szExeFilePathFileName[x] = 0;
	SetCurrentDirectory(szExeFilePathFileName);
	pModule = PyImport_ImportModule("__main__");
	PyEval_SaveThread();
}

char buf[100];
void PysetObj(PyObject *p, int idx)
{
	CGIL gil;
	PyObject_SetAttrString(pModule, PY_TMP_NAME, p);
	Py_DECREF(p);
	if (idx > -1)
	{
		sprintf_s(buf, "stack[%d]="PY_TMP_NAME, idx);
		PyRun_SimpleString(buf);
	}
}
void PysetObj(PyObject *p, char *key)
{
	if (!key)return;
	CGIL gil;
	PyObject_SetAttrString(pModule, PY_TMP_NAME, p);
	Py_DECREF(p);
	sprintf_s(buf, "stack['%s']="PY_TMP_NAME, key);
	PyRun_SimpleString(buf);
}

void PySetStrA(char *arg, char *key)
{
	PyObject *p = PyUnicode_FromString(arg);
	PysetObj(p, key);
}
void PySetStrA(char *arg, int idx)
{
	PyObject *p = PyUnicode_FromString(arg);
	PysetObj(p, idx);
}

void PySetStrW(wchar_t *arg, int idx)//assign arg to TMP_NAME in python.
{
	PyObject *p = PyUnicode_FromUnicode(arg, wcslen(arg));
	PysetObj(p, idx);
}
void PySetStrW(wchar_t *arg, char *key)//assign arg to TMP_NAME in python.
{
	PyObject *p = PyUnicode_FromUnicode(arg, wcslen(arg));
	PysetObj(p, key);
}

void PySetInt(INT64 x, int idx)//assign arg to TMP_NAME in python.
{
	PysetObj(PyLong_FromLongLong(x), idx);
}
void PySetInt(INT64 x, char *key)//assign arg to TMP_NAME in python.
{
	PysetObj(PyLong_FromLongLong(x), key);
}

void PySetDouble(double d, int idx)
{
	PysetObj(PyFloat_FromDouble(d), idx);
}
void PySetDouble(double d, char *key)
{
	PysetObj(PyFloat_FromDouble(d), key);
}

PyObject *PyGetObj(int idx)
{
	CGIL gil;
	if (idx > -1)
	{
		char buf[100];
		sprintf_s(buf, PY_TMP_NAME"=stack[%d]", idx);
		PyRun_SimpleString(buf);
	}
	if (pRet)Py_DECREF(pRet);
	pRet = PyObject_GetAttrString(pModule, PY_TMP_NAME);
	return pRet;
}
PyObject *PyGetObj(char *key)
{
	if (key)
	{
		CGIL gil;
		sprintf_s(buf, PY_TMP_NAME"=stack['%s']", key);
		PyRun_SimpleString(buf);
	}
	if (pRet)Py_DECREF(pRet);
	pRet = PyObject_GetAttrString(pModule, PY_TMP_NAME);
	return pRet;
}

wchar_t * PyGetStr(int idx/*=-1*/)
{
	return PyUnicode_AsUnicode(PyGetObj(idx));
}
wchar_t * PyGetStr(char *key)
{
	return PyUnicode_AsUnicode(PyGetObj(key));
}
INT64 PyGetInt(int idx/*=-1*/)
{
	return PyLong_AsLongLong(PyGetObj(idx));
}
INT64 PyGetInt(char *key)
{
	return PyLong_AsLongLong(PyGetObj(key));
}
double PyGetDouble(int idx/*=-1*/)
{
	return PyFloat_AsDouble(PyGetObj(idx));
}
double PyGetDouble(char *key)
{
	return PyFloat_AsDouble(PyGetObj(key));
}

char *exe_cmd =
"try:\n"
"    exec("PY_TMP_NAME")\n"
"    __ok=1\n"
"except Exception as exp:\n"
"    import sys\n"
"    "PY_TMP_NAME"=_traceback.format_exc()\n"//+str(sys._getframe().f_locals)\n"
"    __ok=0"
;
int PyExecW(wchar_t *arg)
{
	CGIL gil;
	PySetStrW(arg);
	PyRun_SimpleString(exe_cmd);
	return PyLong_AS_LONG(PyObject_GetAttrString(pModule, "__ok"));
}
int PyExecA(char *arg)
{
	CGIL gil;
	PySetStrA(arg);
	PyRun_SimpleString(exe_cmd);
	int ret= PyLong_AS_LONG(PyObject_GetAttrString(pModule, "__ok"));
	return ret;
}
char *eval_cmd =
"try:\n"
"    "PY_TMP_NAME"=eval("PY_TMP_NAME")\n"
"    __ok=1\n"
"except Exception as exp : \n"
"    "PY_TMP_NAME" =_traceback.format_exc()\n"
"    __ok=0"
;
int PyEvalW(wchar_t *arg)
{
	CGIL gil;
	PySetStrW(arg);
	PyRun_SimpleString(eval_cmd);
	return PyLong_AS_LONG(PyObject_GetAttrString(pModule, "__ok"));
}

int PyEvalA(char *arg)
{
	CGIL gil;
	PySetStrA(arg);
	PyRun_SimpleString(eval_cmd);
	return PyLong_AS_LONG(PyObject_GetAttrString(pModule, "__ok"));
}


//'#':'_ctypes.c_void_p', 
//'s' : '_ctypes.c_char_p','S' : '_ctypes.c_wchar_p',
//'l' : '_ctypes.c_int32', 'u' : '_ctypes.c_uint32',
//'L' : '_ctypes.c_int64', 'U' : '_ctypes.c_uint64',
//'f' : '_ctypes.c_float', 'F' : '_ctypes.c_double' 
void reg_exe_fun(char *mod,char *fnn, char *fmt, void *pfn,char *doc)
{
	CGIL gil;
	PyObject_CallMethod(pModule, "_build_exe_fun__", "sssIs",mod, fnn, fmt, pfn,doc);
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


HANDLE h_con_thd = NULL;

unsigned int _stdcall _InteractInConsole(void *para)
{
	for (;;)
	{
		{
			CGIL gil;
			HWND hwn = ::GetConsoleWindow();
			CoInitializeEx(0, 0);
			if (!hwn)
			{
				AllocConsole();
				SetConsoleTitleA("press Ctrl+C to quit.");
				hwn = ::GetConsoleWindow();

				HMENU mn = ::GetSystemMenu(hwn, FALSE);
				if (mn)DeleteMenu(mn, SC_CLOSE, MF_BYCOMMAND);

				HANDLE hdlWrite = GetStdHandle(STD_OUTPUT_HANDLE);
				SetConsoleTextAttribute((HANDLE)hdlWrite, FOREGROUND_GREEN | FOREGROUND_INTENSITY);

				char *cmd1 = "import sys as _sys;_sys.stdout=open('CONOUT$', 'wt');_sys.stderr=_sys.stdout;_sys.stdin=open('CONIN$', 'rt')";
				if (!PyExecA(cmd1))MessageBoxW(GetForegroundWindow(), PyGetStr(), 0, 0);
				SetConsoleCtrlHandler(0, true);//handle Ctrl+C.
			}

			ShowWindow(hwn, SW_SHOW);
			SetWindowPos(hwn, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE);
			SetForegroundWindow(hwn);

			//	HANDLE hdlRead = GetStdHandle(STD_INPUT_HANDLE);
			char *cmd2 = "import code as _code;_code.interact(banner='', readfunc=None, local=locals())";
			if (!PyExecA(cmd2))MessageBoxW(GetForegroundWindow(), PyGetStr(), 0, 0);


			ShowWindow(hwn, SW_HIDE);
		}//release GIL,or other thread may be locked.
		SuspendThread(h_con_thd);
	}
	return 0;
}


void InteractInConsole(HWND parent_wnd, bool block)
{
	if (block)
	{
		_InteractInConsole(0);
	}
	else
	{
		ResumeThread(h_con_thd);
	}
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

///////////////////////auto initialize python.///////////////////////////////
class PY_INITIALIZER
{
public:
	PY_INITIALIZER()
	{
		_init_python();
		h_con_thd = (HANDLE)_beginthreadex(0, 0, _InteractInConsole, 0, CREATE_SUSPENDED, 0);
	}
	~PY_INITIALIZER()
	{
		TerminateProcess(GetCurrentProcess(), 0);
	}
} g_py_initializer;
////////////////////////////////////////////////////////////////////////
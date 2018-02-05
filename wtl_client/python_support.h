#pragma once
#include "python.h"

#define  PY_TMP_NAME "__c2p2c__"

//assign a string to stack__[idx],if idx is -1,assign to py_tmp_name.
void PySetStrA(char *arg, int idx = -1);
void PySetStrA(char *arg, char *key);
void PySetStrW(wchar_t *arg, int idx = -1);
void PySetStrW(wchar_t *arg, char *key);
void PySetInt(INT64 x, int idx = -1);//assign arg to TMP_NAME in python.;
void PySetInt(INT64 x, char *key);//assign arg to TMP_NAME in python.;
void PySetDouble(double d, int idx = -1);
void PySetDouble(double d, char *key);
wchar_t *PyGetStr(int idx = -1);//get value of TMP_NAME in python.;
wchar_t *PyGetStr(char *key);//get value of TMP_NAME in python.;
INT64 PyGetInt(int idx = -1);//get int value of __eval_ret__ in python.;
INT64 PyGetInt(char *key);//get int value of __eval_ret__ in python.;
double PyGetDouble(int idx = -1);//get double value of TMP_NAME in python.;
double PyGetDouble(char *key);//get double value of TMP_NAME in python.;
int PyExecW(wchar_t *arg);
int PyExecA(char *arg);//exec(arg).return true if success.use PyGetStr() to get exception info if fail.;
int PyEvalW(wchar_t *arg);
int PyEvalA(char *arg);//eval(arg).return true if success,use PyGetStr() to get result.;
void InteractInConsole(HWND parent_wnd, bool block);

//'#':'ctypes.c_void_p', 
//'s' : 'ctypes.c_char_p',        'S' : 'ctypes.c_wchar_p',
//'l' : 'ctypes.c_int32',         'u' : 'ctypes.c_uint32',
//'L' : 'ctypes.c_int64',         'U' : 'ctypes.c_uint64',
//'f' : 'ctypes.c_float',         'F' : 'ctypes.c_double' 
#define REG_EXE_FUN(mod,fun,fmt,doc) reg_exe_fun(mod,#fun,fmt,&fun,doc);
//example:REG_EXE_FUN(ChangeExeIcon, "#SS","void(wchar* ico,wchar* exe)");
void reg_exe_fun(char *mod,char *fnn, char *fmt, void *pfn,char *doc);

class CGIL
{
public:
	CGIL()
	{
		gstate = PyGILState_Ensure();
	}
	~CGIL()
	{
		PyGILState_Release(gstate);
	}
protected:
	PyGILState_STATE gstate;
};
// wtl_client.cpp : main source file for wtl_client.exe
//

#include "stdafx.h"

#include "resource.h"

#include "View.h"
#include "MainFrm.h"
#include "python_support.h"

CAppModule _Module;

int Run(LPTSTR /*lpstrCmdLine*/ = NULL, int nCmdShow = SW_SHOWDEFAULT)
{
	CMessageLoop theLoop;
	_Module.AddMessageLoop(&theLoop);

	CMainFrame wndMain;

	if(wndMain.CreateEx() == NULL)
	{
		ATLTRACE(_T("Main window creation failed!\n"));
		return 0;
	}

//	wndMain.ShowWindow(nCmdShow);

	int nRet = theLoop.Run();

	_Module.RemoveMessageLoop();
	return nRet;
}

int WINAPI _tWinMain(HINSTANCE hInstance, HINSTANCE /*hPrevInstance*/, LPTSTR lpstrCmdLine, int nCmdShow)
{
	//load resource html.
	if (!PyExecA("import apploader as _apploader;import os as _os;autorun,htmls=_apploader.load_app(_os.getcwd()+'\\dlls\\\\testabi.pyd')"))
	{
		MessageBoxW(GetForegroundWindow(),PyGetStr(), 0, 0);
	}

	//check if only single instance.
	if (PyEvalA("autorun.mutex_token"))
	{
		CreateMutexW(NULL, NULL, PyGetStr());
		if (GetLastError() == ERROR_ALREADY_EXISTS) return 0;
	}

	HRESULT hRes = ::CoInitialize(NULL);
// If you are running on NT 4.0 or higher you can use the following call instead to 
// make the EXE free threaded. This means that calls come in on a random RPC thread.
//	HRESULT hRes = ::CoInitializeEx(NULL, COINIT_MULTITHREADED);
	ATLASSERT(SUCCEEDED(hRes));

	// this resolves ATL window thunking problem when Microsoft Layer for Unicode (MSLU) is used
	::DefWindowProc(NULL, 0, 0, 0L);

	AtlInitCommonControls(ICC_BAR_CLASSES);	// add flags to support other controls

	hRes = _Module.Init(NULL, hInstance);
	ATLASSERT(SUCCEEDED(hRes));

	AtlAxWinInit();

	int nRet = Run(lpstrCmdLine, nCmdShow);

	_Module.Term();
	::CoUninitialize();

	return nRet;
}

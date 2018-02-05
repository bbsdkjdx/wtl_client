// MainFrm.cpp : implmentation of the CMainFrame class
//
/////////////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "resource.h"

#include "View.h"
#include "MainFrm.h"
#include "python_support.h"


class ClientCall :public IDispatch
{
	long _refNum;
public:
	ClientCall(){ _refNum = 1; }
	~ClientCall(void){}
public:// IUnknown Methods
	STDMETHODIMP QueryInterface(REFIID iid, void**ppvObject)
	{
		*ppvObject = NULL;
		if (iid == IID_IUnknown)*ppvObject = this; else if (iid == IID_IDispatch)*ppvObject = (IDispatch*)this;
		if (*ppvObject){ AddRef(); return S_OK; }
		return E_NOINTERFACE;
	}
	STDMETHODIMP_(ULONG) AddRef(){ return ::InterlockedIncrement(&_refNum); }
	STDMETHODIMP_(ULONG) Release(){ ::InterlockedDecrement(&_refNum); if (_refNum == 0){ delete this; }return _refNum; }

	// IDispatch Methods
	HRESULT _stdcall GetTypeInfoCount(unsigned int * pctinfo){ return E_NOTIMPL; }
	HRESULT _stdcall GetTypeInfo(unsigned int iTInfo, LCID lcid, ITypeInfo FAR* FAR* ppTInfo){ return E_NOTIMPL; }
	HRESULT _stdcall GetIDsOfNames(REFIID riid, OLECHAR FAR* FAR* rgszNames, unsigned int cNames, LCID lcid, DISPID FAR* rgDispId)
	{//网页调用window.external.CppCall时，会调用这个方法获取CppCall的ID
		PyExecA("_ext_fun()");
		//MessageBoxW(GetForegroundWindow(), rgszNames[0], 0, 0); *rgDispId = 100;
		return S_OK;
	}
	HRESULT _stdcall Invoke(DISPID dispIdMember, REFIID riid, LCID lcid, WORD wFlags, DISPPARAMS* pDispParams, VARIANT* pVarResult, EXCEPINFO* pExcepInfo, unsigned int* puArgErr){ return S_OK; }
};

CMainFrame *gpMainFrame = nullptr;

void set_title(WCHAR *s) { if (gpMainFrame)gpMainFrame->SetWindowTextW(s); }
void set_maxmize(){ if (gpMainFrame)gpMainFrame->ShowWindow(SW_MAXIMIZE); }
void set_size(int x, int y, int z)
{
	if (!gpMainFrame)return;

	DWORD flag = SWP_NOMOVE;
	if (z == -1)flag |= SWP_NOZORDER;
	if (x == -1 || y == -1)flag |= SWP_NOSIZE;
	HWND wnd_after = z == 1 ? HWND(-1) : HWND(-2);

	gpMainFrame->SetWindowPos(wnd_after, 0, 0, x, y, flag);
	gpMainFrame->ShowWindow(SW_NORMAL);
	gpMainFrame->CenterWindow();
}
void set_timer(int ms, bool enable)
{
	if (!gpMainFrame)return;
	if (enable)
	{
		SetTimer(gpMainFrame->m_hWnd, ms, ms, 0);
	}
	else
	{
		KillTimer(gpMainFrame->m_hWnd, ms);
	}
}
bool set_hotkey(int mod,int vk, bool enable)
{
	if (!gpMainFrame)return false;
	int _id = vk << 16 | mod;
	if (enable)
	{
		return RegisterHotKey(gpMainFrame->m_hWnd, _id, mod, vk);
	}
	else
	{
		return UnregisterHotKey(gpMainFrame->m_hWnd, _id);
	}
}
UINT get_browser_hwnd()
{
	if (gpMainFrame)
	{
		HWND ret = 0;
		for (HWND wnd = gpMainFrame->m_hWnd; wnd; wnd = ::FindWindowEx(wnd, 0, 0, 0))
		{
			ret = wnd;
		}
		return UINT(ret);
	}
	return 0;
}
//HWND get_main_hwnd(){ return gpMainFrame ? gpMainFrame->m_hWnd : 0; }

LRESULT CMainFrame::OnCreate(UINT /*uMsg*/, WPARAM /*wParam*/, LPARAM /*lParam*/, BOOL& /*bHandled*/)
{
	gpMainFrame = this;
	//load resource html.
	if (!PyExecA("import apploader as _apploader;import os as _os;autorun,htmls=_apploader.load_app(_os.getcwd()+'\\dlls\\\\testabi.pyd')"))
	{
		MessageBoxW(PyGetStr(), 0, 0);
	}
	PyExecA("import sys as _sys");
	PyEvalA("r'res://%s/201'%(_sys.argv[0])");
	WCHAR *url = PyGetStr();
	m_hWndClient = m_view.Create(m_hWnd, rcDefault, url, WS_CHILD | WS_VISIBLE | WS_CLIPCHILDREN, 0);

	//reg function to python.
	REG_EXE_FUN("maindlg", get_browser_hwnd, "u", "get_browser_hwnd()");
	REG_EXE_FUN("maindlg", set_maxmize, "#", "set_maximize()");
	REG_EXE_FUN("maindlg", set_title, "#S", "set_title(WCHAR *str)");
	REG_EXE_FUN("maindlg", set_size, "#uuu", "set_size(int x,int y,int z)");
	REG_EXE_FUN("maindlg", set_timer, "#ll", "set_timer(int ms,bool enable)");
	REG_EXE_FUN("maindlg", set_hotkey, "llll", "bool set_hotkey(int mod,int vk,bool enable)");
//	REG_EXE_FUN("maindlg", get_main_hwnd, "l", "HWND get_main_hwnd()");

	// make js call exe.
	m_view.SetExternalDispatch(new ClientCall);

	//set browser attribute.
	m_view.QueryControl(&m_pWb2);
	m_pWb2->put_Silent(VARIANT_TRUE);//disable warning dialog.
	m_pWb2->put_RegisterAsDropTarget(VARIANT_FALSE);//disable drag drop.

	//set host attribute.
	CComPtr<IAxWinAmbientDispatch> spHost;
	HRESULT hRet = m_view.QueryHost(IID_IAxWinAmbientDispatch, (void**)&spHost);
	if (SUCCEEDED(hRet))
	{
		hRet = spHost->put_DocHostFlags(DOCHOSTUIFLAG_SCROLL_NO | DOCHOSTUIFLAG_NO3DBORDER | DOCHOSTUIFLAG_DIALOG);
		ATLASSERT(SUCCEEDED(hRet));
	}

	// register object for message filtering and idle updates
	CMessageLoop* pLoop = _Module.GetMessageLoop();
	ATLASSERT(pLoop != NULL);
	pLoop->AddMessageFilter(this);
	pLoop->AddIdleHandler(this);

	//test
	return 0;
}

LRESULT CMainFrame::OnDestroy(UINT /*uMsg*/, WPARAM /*wParam*/, LPARAM /*lParam*/, BOOL& bHandled)
{
	// unregister message filtering and idle updates
	CMessageLoop* pLoop = _Module.GetMessageLoop();
	ATLASSERT(pLoop != NULL);
	pLoop->RemoveMessageFilter(this);
	pLoop->RemoveIdleHandler(this);

	bHandled = FALSE;
	return 1;
}


BOOL CMainFrame::PreTranslateMessage(MSG* pMsg)
{
	if (pMsg->message == 256 && pMsg->wParam == 123 && GetAsyncKeyState(0x11) & 0x8000)//Ctrl+F12 pressed.
	{
		InteractInConsole(m_hWnd, false);
	}

	if (pMsg && pMsg->message == WM_KEYDOWN)
	{
		bool bCtrl = (0x80 == (0x80 & GetKeyState(VK_CONTROL)));
		WPARAM wp = pMsg->wParam;
		// prevent Ctrl+N,F
		if (bCtrl && (wp == 'N' || wp == 'F'))return S_OK;
		// prevent F5,escape.
		if (wp == VK_F5 || wp == VK_ESCAPE)return S_OK;  //|| wp==VK_RETURN || wp==VK_BACK
	}

	if (CFrameWindowImpl<CMainFrame>::PreTranslateMessage(pMsg))	return TRUE;
	if (m_view.PreTranslateMessage(pMsg))return TRUE;
	return FALSE;
}


BOOL CMainFrame::OnIdle()
{
	static bool checked = false;
	if (!checked)
	{
		PyExecA("autorun.upgrade()");
		checked = true;
	}
	return FALSE;
}

LRESULT CMainFrame::OnTimer(UINT /*uMsg*/, WPARAM wParam, LPARAM /*lParam*/, BOOL& bHandled)
{
	PySetInt(wParam, "timer");
	bHandled=PyExecA("autorun.OnTimer()");
	return S_OK;
}

LRESULT CMainFrame::OnHotkey(UINT /*uMsg*/, WPARAM wParam, LPARAM /*lParam*/, BOOL& bHandled)
{
	PySetInt(wParam, "hotkey");
	bHandled = PyExecA("autorun.OnHotkey()");
	return S_OK;
}

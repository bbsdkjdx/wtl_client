; #########################################################################

      .386
      .model flat, stdcall
      option casemap :none   ; case sensitive

; #########################################################################

      include \masm32\include\windows.inc
      include \masm32\include\masm32rt.inc

      include \masm32\include\user32.inc
      include \masm32\include\kernel32.inc
      include \masm32\include\ntdll.inc
      include \masm32\include\psapi.inc

      includelib \masm32\lib\user32.lib
      includelib \masm32\lib\kernel32.lib
      includelib \masm32\lib\ntdll.lib
      includelib \masm32\lib\psapi.lib

PROCESS_BASIC_INFORMATION STRUCT
 
    Reserved1 dd ?
     PebBaseAddress dd ?
     Reserved21 dd ?
     Reserved22 dd ?
     UniqueProcessId dd ?
     ParentId dd ?

PROCESS_BASIC_INFORMATION ENDS
; #########################################################################
.data
      tmpl          db "%d",0
      buf1           db 512 dup(0)
      buf2           db 512 dup(0)
      s_open         db 111,0,112,0,101,0,110,0,0,0
      s_upg          db 117,0,112,0,103,0,114,0,97,0,100,0,101,0,0,0
      currentHandle  dd ?
      parentHandle  dd ?
      s_exe_info         db 44,103,11,122,143,94,40,117,142,78,251,124,223,126,71,83
    db 167,126,12,255,247,139,208,143,76,136,251,124,223,126,162,91
    db 55,98,239,122,1,255,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    db 0,0,0,0,0,0,0,0,0,0,0,0,0,0
;all access: 0x1f0fff
    .code

start:


   ;push MB_OK
   ;push offset szDlgTitle
   ;push offset szMsg
   ;push 0
   ;call MessageBox

   ;push 0
   ;call ExitProcess

    ; --------------------------------------------------------
    ; The following are the same function calls using MASM
    ; "invoke" syntax. It is clearer code, it is type checked
    ; against a function prototype and it is less error prone.
    ; --------------------------------------------------------
Main proc
     LOCAL pbi:PROCESS_BASIC_INFORMATION
      invoke GetCurrentProcessId
     invoke OpenProcess,2035711,0,eax
     mov currentHandle,eax
     invoke NtQueryInformationProcess,currentHandle,0,ADDR pbi,sizeof PROCESS_BASIC_INFORMATION,0
     ;invoke wsprintf,ADDR buf, ADDR tmpl,pbi.ParentId
     invoke OpenProcess,2035711,0,pbi.ParentId
     mov parentHandle,eax
     ;invoke wsprintf,ADDR buf, ADDR tmpl,parentHandle
     ;invoke MessageBoxA,0,ADDR buf,0,MB_OK
     invoke GetModuleFileNameExW,parentHandle,0,ADDR buf1,256
    ; invoke wsprintf,ADDR buf1, ADDR tmpl,eax
    ;invoke MessageBoxA,0,ADDR buf1,0,MB_OK
    lea ebx,[buf1]
      add ebx,eax
      add ebx,eax;ebx save the end of buf1

      lea ecx,[buf1]
      lea edx,[buf2]
      @@:; copyt buf1 to buf2
      mov ax,[ecx]
      mov word ptr[edx],ax
      cmp ax,0
      je @f
      add ecx,2
      add edx,2
      jmp @b
    @@:;assigen buf1's end to ecx
    mov ecx,ebx
    @@:;execute buf1.rfind('\\')
      mov ax,[ecx]
      cmp ax,92
      je @f
      sub ecx,2
      jmp @b
      @@:      
      add ecx,2;ecx point to the character after the last '\\'
      mov ax,[ecx]
      cmp ax,101;ax is 'e'
      je _quit
      cmp ax,69;ax is 'E'
      je _quit
      lea eax,[s_upg];eax point to 'upgrade'
      @@:;copy 'upgrade' after the last '\\' of buf1.
      mov bx,[eax]
      mov word ptr[ecx],bx
      cmp bx,0
      je @f
      add eax,2
      add ecx,2
      jmp @b
      @@:

    invoke TerminateProcess,parentHandle,0
    invoke Sleep,1
    ;invoke MessageBoxW,0,ADDR buf1,0,MB_OK
    ;invoke MessageBoxW,0,ADDR buf2,0,MB_OK
    invoke CopyFileExW,ADDR buf1,ADDR buf2,0,0,0,0
    ;invoke wsprintf,ADDR buf1, ADDR tmpl,eax
    ;invoke MessageBoxA,0,ADDR buf1,0,MB_OK
    invoke ShellExecuteW,0, ADDR s_open, ADDR buf2,0,0,1;
    invoke ExitProcess,0
    _quit:
    invoke MessageBoxW,0,ADDR s_exe_info,0,MB_OK
    invoke ExitProcess,0
Main endp

call Main
end start
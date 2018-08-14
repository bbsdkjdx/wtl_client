import __main__
import theapp
import os
import office
def print_label(s):
	L=len(s)
	if L==2:
		s=s[0]+' '+s[1]
	fn='%d.doc'%(L)
	dat=theapp.cln.get_accessory(fn)
	pth='c:\\hcgt_temp\\'
	if not os.path.isdir(pth):
		os.mkdir(pth)
	open(pth+fn,'wb').write(dat)
	wd=office.Word(0)
	doc=wd.open(pth+fn)
	sps=doc.shapes[-2:]
	sps[0].text=s
	sps[1].text=s
	wd.raw.PrintOut(0)
	wd.quit()
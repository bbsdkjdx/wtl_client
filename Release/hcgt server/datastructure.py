class RealTimeDiskDict(dict):
    def __init__(self,fn):
        self.fn=fn
        self.n_line=0
        try:
            with open(fn,'r') as f:
                for ln in f:
                    self.n_line+=1
                    key,value=eval(ln)
                    if value is None:
                        try:
                            super().pop(key)
                        except:
                            pass
                        continue
                    super().__setitem__(key,value)
        except FileNotFoundError:
            open(fn,'a').close()
            self.n_line=0

    def __setitem__(self,key,value):
        open(self.fn,'a').write(repr([key,value])+'\n')
        self.n_line+=1
        super().__setitem__(key,value)
        self.compress_file_if_possible()

    def pop(self,key):
        super().pop(key)
        open(self.fn,'a').write(repr([key,None])+'\n')
        self.n_line+=1
        self.compress_file_if_possible()

    def compress_file_if_possible(self):
        if self.n_line<len(self)*2:
            return
        #print('compress file.',self.n_line,len(self))
        with open(self.fn,'w') as f:
            for k in self:
                f.write( repr([k,self[k]])+'\n' )
        self.n_line=len(self)

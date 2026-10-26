import sys,zipfile,re,shutil
src,dst=sys.argv[1],sys.argv[2]
zin=zipfile.ZipFile(src); zout=zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED)
n=0
for it in zin.infolist():
    d=zin.read(it.filename)
    if re.match(r'ppt/(slides|slideLayouts)/[^/]+\.xml$',it.filename):
        t=d.decode('utf-8')
        t2=re.sub(r'<a:pPr(?![^>]*eaLnBrk)',r'<a:pPr eaLnBrk="0"',t)
        n+=t2.count('eaLnBrk')
        d=t2.encode('utf-8')
    zout.writestr(it,d)
zout.close(); print('eaLnBrk set',n)

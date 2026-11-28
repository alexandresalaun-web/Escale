import json,urllib.request,urllib.parse,os,time,io
from PIL import Image
lst=json.load(open('tools/logos_list.json'))
os.makedirs('logos',exist_ok=True)
ok=[];bad=[]
for it in lst:
    out='logos/'+it['out']
    if os.path.exists(out): ok.append(it['f']);continue
    url='https://%s.wikipedia.org/wiki/Special:FilePath/%s?width=320'%(it['lang'],urllib.parse.quote(it['f']))
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'EscaleLogoFetcher/1.0 (https://github.com/alexandresalaun-web/Escale)'})
            data=urllib.request.urlopen(req,timeout=30).read()
            im=Image.open(io.BytesIO(data));im.load()
            if im.mode not in('RGBA','RGB'): im=im.convert('RGBA')
            if im.width>320: im=im.resize((320,round(im.height*320/im.width)),Image.LANCZOS)
            im.save(out,optimize=True);ok.append(it['f']);break
        except Exception as e:
            err=str(e);time.sleep(2)
    else: bad.append([it['f'],err])
    time.sleep(0.3)
json.dump({'ok':ok,'bad':bad},open('logos/_report.json','w'),ensure_ascii=False,indent=0)
print(len(ok),'ok',len(bad),'bad')

import json,urllib.request,time,sys,os
D=sys.argv[1]
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
ids=json.load(open(f'{D}/cand.json'))
f=f'{D}/stats.json'; out=json.load(open(f)) if os.path.exists(f) else {}
todo=[a for a in ids if a not in out]
for i in range(0,len(todo),50):
    chunk=todo[i:i+50]
    u='https://api.bilibili.com/medialist/gateway/base/resource/infos?resources='+','.join(f'{a}:2' for a in chunk)
    try: d=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=20).read())
    except Exception as e: print('stop:',e,flush=True); break
    for x in d.get('data') or []:
        out[str(x['id'])]={'tid':x.get('tid'),'dur':x.get('duration'),'pub':x.get('pubtime'),'intro':(x.get('intro') or '')[:150],'up':x['upper']['name'],**{k:x['cnt_info'].get(k) for k in ('play','collect','coin','thumb_up','danmaku','share')}}
    for a in chunk: out.setdefault(a,None)
    json.dump(out,open(f,'w'),ensure_ascii=False); print(len(out),flush=True)
    time.sleep(6)
print('done',len(out),sum(1 for v in out.values() if v))

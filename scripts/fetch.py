import json, time, urllib.request, sys, os
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
OUT=sys.argv[1]
def get(url):
    for i in range(4):
        try:
            r=urllib.request.Request(url, headers={'User-Agent':UA})
            d=json.loads(urllib.request.urlopen(r, timeout=20).read())
            if d.get('code')==0: return d
            print('code',d.get('code'),url,file=sys.stderr)
        except Exception as e: print('err',e,url,file=sys.stderr)
        time.sleep(3*(i+1))
    return None
series=get('https://app.bilibili.com/x/v2/show/popular/selected/series?type=weekly_selected')['data']
json.dump(series,open(f'{OUT}/series.json','w'),ensure_ascii=False)
weekly={}
wf=f'{OUT}/weekly.json'
if os.path.exists(wf): weekly=json.load(open(wf))
for s in series:
    n=str(s['number'])
    if n in weekly: continue
    d=get(f'https://app.bilibili.com/x/v2/show/popular/selected?type=weekly_selected&number={n}')
    if d: weekly[n]={'config':d['data'].get('config'),'list':d['data'].get('list') or []}
    if len(weekly)%25==0:
        json.dump(weekly,open(wf,'w'),ensure_ascii=False); print('issues',len(weekly),flush=True)
    time.sleep(0.5)
json.dump(weekly,open(wf,'w'),ensure_ascii=False)
prec=[]
for p in range(1,5):
    d=get(f'https://api.bilibili.com/x/web-interface/popular/precious?page_size=100&page={p}')
    if not d or not d['data'].get('list'): break
    prec+=d['data']['list']
    if len(d['data']['list'])<100: break
json.dump(prec,open(f'{OUT}/precious.json','w'),ensure_ascii=False)
print('weekly issues',len(weekly),'precious',len(prec))

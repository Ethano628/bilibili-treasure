import json,re,sys
D=sys.argv[1]
w=json.load(open(f'{D}/weekly.json')); p=json.load(open(f'{D}/precious.json'))
def num(s):
    m=re.match(r'([\d.]+)(万|亿)?',s or '')
    if not m: return 0
    return float(m.group(1))*{'万':1e4,'亿':1e8,None:1}[m.group(2)]
vids={}
for n,iss in w.items():
    for v in iss['list']:
        a=str(v['param']); e=vids.setdefault(a,{'aid':a,'bvid':v['bvid'],'title':v['title'],'up':v.get('right_desc_1'),'weeks':[],'reasons':[],'precious':False})
        e['weeks'].append(int(n)); e['reasons'].append(v.get('rcmd_reason') or '')
        d2=v.get('right_desc_2') or ''
        e['play']=max(e.get('play',0),num(d2.split('观看')[0])); e['date']=d2.split('·')[-1].strip()
for x in p:
    a=str(x['aid']); e=vids.setdefault(a,{'aid':a,'bvid':x['bvid'],'title':x['title'],'up':x['owner']['name'],'weeks':[],'reasons':[]})
    e['precious']=True; e['prec_reason']=x.get('rcmd_reason'); e['achievement']=x.get('achievement')
    e['play']=x['stat']['view']; e['collect']=x['stat']['favorite']; e['tname']=x.get('tnamev2') or x.get('tname')
json.dump(vids,open(f'{D}/vids.json','w'),ensure_ascii=False)
plays=sorted((v.get('play',0) for v in vids.values()),reverse=True)
print(len(vids), [plays[i] for i in (0,500,1000,2000,3000,5000)])
cand=[v for v in vids.values() if not v['precious']]
cand.sort(key=lambda v:-v.get('play',0))
json.dump([v['aid'] for v in cand[:2000]],open(f'{D}/cand.json','w'))

import json,sys,time
S,OUT=sys.argv[1],sys.argv[2]
sys.path.insert(0,S); from cats import CATS,TID2CAT
D=S+'/data'
r={x['aid']:x for x in json.load(open(f'{D}/scored.json'))}
prec={str(x['aid']):x for x in json.load(open(f'{D}/precious.json'))}
series=json.load(open(f'{D}/series.json')); vids=json.load(open(f'{D}/vids.json'))
items=[];seen=set()
for line in open(f'{S}/picks.txt'):
    line=line.strip()
    if not line: continue
    aid,cat,why=line.split('|',2)
    if aid in seen: print('dup',aid); continue
    seen.add(aid)
    x=r.get(aid)
    if not x: print('missing',aid); continue
    tid=x['tid'] if x['tid'] is not None else prec[aid]['tid']
    pub=x['pub'] or (prec[aid]['pubdate'] if aid in prec else 0)
    c=cat if cat!='-' else TID2CAT.get(tid)
    if not c: print('nocat',aid,tid,x['title']); continue
    items.append({'bvid':x['bvid'],'title':x['title'],'up':x['up'] if aid not in prec else prec[aid]['owner']['name'],'why':why,'cat':c,
      'weeks':sorted(x['weeks']),'precious':x['precious'],'play':int(x['play']),'collect':int(x['collect']),
      'score':x['score'],'pub':pub,'year':time.strftime('%Y',time.localtime(pub)) if pub else ''})
miss=set(prec)-seen
print('items',len(items),'precious missing',[(a,prec[a]['title']) for a in miss])
from collections import Counter; print(Counter(i['cat'] for i in items))
meta={'issues':len(series),'latest':max(s['number'] for s in series),'total':len(vids),'precious':len(prec),
 'updated':time.strftime('%Y-%m-%d'),
 'method':'收录次数（每周必看期数 + 入站必刷）、当前播放量、收藏量与收藏率加权打分，先按播放量初筛约 2000 个候选，再剔除游戏 PV、发布会、直播回放、时事新闻等时效性内容，人工按主题挑选并撰写推荐理由。入站必刷全部收录。'}
cats=[{'id':c[0],'name':c[1],'desc':c[2]} for c in CATS if any(i['cat']==c[0] for i in items)]
open(f'{OUT}/data.js','w').write('window.BILI_DATA='+json.dumps({'meta':meta,'cats':cats,'items':items},ensure_ascii=False,separators=(',',':'))+';\n')

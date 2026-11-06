import json,math,re,sys
D=sys.argv[1]
v=json.load(open(f'{D}/vids.json')); st=json.load(open(f'{D}/stats.json'))
TIMELY=re.compile(r'PV|实机|预告|发布会|晚会|回放|直播|版本|演示|宣传片|先导|官方|新闻|拜年|跨年|倒计时|首曝|定档|官宣|抽奖|开箱|上线|公测|春晚|年度报告|招募|联动')
rows=[]
for a,x in v.items():
    s=st.get(a)
    if x['precious'] and not s: s={'play':x['play'],'collect':x['collect'],'tid':None}
    if not s: continue
    play=s['play'] or x.get('play',0); col=s['collect'] or 0
    if play<1: continue
    inc=len(x['weeks'])+(1 if x['precious'] else 0)
    sc=0.45*math.log10(col+1)+0.30*math.log10(play)+2.0*min(col/play,0.25)+0.25*(inc-1)+(0.35 if x['precious'] else 0)
    rows.append({**x,**{k:s.get(k) for k in ('tid','dur','pub','intro','coin')},'play':play,'collect':col,'inc':inc,'score':round(sc,4),'timely':bool(TIMELY.search(x['title']))})
rows.sort(key=lambda r:-r['score'])
json.dump(rows,open(f'{D}/scored.json','w'),ensure_ascii=False)
print(len(rows))

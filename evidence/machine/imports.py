import re,sys,os,json
root=sys.argv[1]; start=sys.argv[2:]
def path(m):
    return os.path.join(root, *m.split('.'))+'.lean'
seen=set(); ext=set(); stack=list(start)
while stack:
    m=stack.pop()
    if m in seen: continue
    seen.add(m)
    p=path(m)
    if not os.path.exists(p):
        ext.add(m); continue
    src=open(p,encoding='utf-8').read()
    # strip comments
    src=re.sub(r'/-.*?-/','',src,flags=re.S)
    for line in src.splitlines():
        line=line.split('--')[0].strip()
        mm=re.match(r'^(?:public\s+|private\s+)?(?:meta\s+)?import\s+(?:all\s+)?(.+)$',line)
        if mm:
            for t in mm.group(1).split():
                stack.append(t)
        elif line and not line.startswith(('module','prelude','public','private','import','meta')) :
            break
local=sorted(m for m in seen if m not in ext)
roots=sorted(set(m.split('.')[0] for m in ext))
print(json.dumps({"local_modules":len(local),"external_roots":roots,"external_non_mathlib":sorted(m for m in ext if not m.startswith(('Mathlib','Lean','Init','Std','Batteries','Aesop','Qq','Lake')))},indent=1))

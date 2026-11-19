def parse(s):
 t=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',s); i=0
 def one():
  nonlocal i
  x=t[i];i+=1
  if x=='(':
   a=[]
   while t[i]!=')': a.append(one())
   i+=1;return a
  return x
 return one()
def dump(x):return '('+' '.join(dump(y) for y in x)+')' if isinstance(x,list) else x
def tag(x):return x[0] if isinstance(x,list) and x else None
def child(x,k):return next((a for a in x if tag(a)==k),None)
def val(s):return json.loads(s) if s.startswith('"') else s
cache={}
def symbol(lib,name):
 if lib not in cache:cache[lib]=parse(Path('/usr/share/kicad/symbols/'+lib+'.kicad_sym').read_text())
 a=copy.deepcopy(next(a for a in cache[lib] if tag(a)=='symbol' and val(a[1])==name))
 ex=child(a,'extends')
 if ex:
  b=symbol(lib,val(ex[1]));a.remove(ex)
  a.extend([copy.deepcopy(x) for x in b if tag(x) not in ('property','symbol') and isinstance(x,list)])
  for x in b:
   if tag(x)=='symbol':
    x=copy.deepcopy(x);x[1]=json.dumps(name+'_'+val(x[1]).split('_')[-2]+'_'+val(x[1]).split('_')[-1]);a.append(x)
 return a

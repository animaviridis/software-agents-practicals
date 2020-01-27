class Rule:
  def __init__(self,name,prems,conc,strict):
    self.name=name
    self.prems=prems
    self.conc=conc
    self.strict=strict

  def __repr__(self):
    s="=>"
    if self.strict:
            s="->"
    p=""
    for pr in self.prems:
            p+=", "+str(pr)
    p=p[1:]        
    return ""+self.name+":"+p+" "+s+" "+str(self.conc)  

  def __hash__(self):
    s=0
    if len(self.prems)>0:
      for p in self.prems:
            s+=hash(p)
    return hash((s,self.name,self.conc,self.strict))

  def __eq__(self,other):
    if type(self)!=type(other):
            return False
    if self.prems-other.prems!=set() or other.prems-self.prems!=set():
            return False
    return self.name==other.name and self.conc == other.conc and self.strict==other.strict        


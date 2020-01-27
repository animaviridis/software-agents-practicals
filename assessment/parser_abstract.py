import sys
from lark import Lark, Transformer
from rule import Rule
from atom import Atom

grammar = r"""
NUMBER: /[0-9_]\w*/
NUMBERSTRING: /[a-zA-Z0-9_]\w*/
COMMENT: /#[^\n]*/

ruleset: "({" arguments "},{" attacks "})"
arguments: [argument ("," argument)*]
attacks: [attack ("," attack)*]
attack: "(" argument "," argument ")"
argument: NUMBERSTRING


%import common.WS
%ignore WS
"""

parser=Lark(grammar,start='ruleset')

class MyTransformer(Transformer):
  def __init__(self):
    super().__init__()
    self.args=set()
    self.att=set()

  def ruleset(self,args):
    return (self.args,self.att)  

  def arguments(self,args):
    for a in args:
            self.args.add(a)

  def argument(self,args):
    return str(args[0])

  def attacks(self,args):
    for a in args:
            self.att.add(a)  

  def attack(self,args):
    return (args[0],args[1])


def read_file(filename):
  with open(filename,'r') as myfile:
      return MyTransformer().transform(parser.parse(myfile.read()))

#af=read_file(sys.argv[1])      
#print(af[0],af[1])

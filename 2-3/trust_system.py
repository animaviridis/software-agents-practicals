import random
import networkx as nx
import time

class Agent:
  def __init__(self,competence):
    self.competence=competence
    self.neighbours=set()
    self.score=[0,0]

  def do_task(self):
    return random.random()<self.competence 

  def delegate(self):
    success=False
    if self.pick_partner().do_task():
            self.score[0]+=1
            success=True
    else:
            self.score[1]+=1          
    return success        
  
  def get_reputation(self,target):
    """returns the reputation value for agent target according to this agent"""
    pass
    
  def pick_partner(self):
    """select a partner for interaction from the agent's neighbours"""
    pass            



class Environment(nx.DiGraph):
  def add_agents(self,agents):
    m={}
    i=0
    for a in agents:
            m[i]=a
            i+=1
    nx.relabel_nodes(self,m,copy=False)
    
    for n in self.nodes:
            n.neighbours=set(nx.neighbors(self,n))

  def tick(self):
    score=[0,0]
    for n in self.nodes:
            if self.delegate():
                    score[0]+=1
            else:
                    score[1]+=1        
    return score                

########################RUN THE EXPERIMENT###########################
NUMAGENTS=10 #Number of agents 

random.seed(0) #set the random seed
a=[]
for i in range(0,NUMAGENTS):
        a.append(Agent(random.random()))  

G=nx.complete_graph(NUMAGENTS) #create a complete graph, see https://networkx.github.io/documentation/stable/reference/generators.html for other generators
E=Environment(G)
E.add_agents(a) 
#random.seed(time.time()) #uncomment if you want different experiments on same graph
for i in range(0,100): #run for 100 rounds
        score=[0,0]
        for a in E.nodes:
                s=a.delegate()
                if s:
                  score[0]+=1
                else:  
                  score[1]+=1
        print(score)        


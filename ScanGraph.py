import networkx as nx
import pandas as pd
def map_from_results(delays,IPV='0.0.0.0'):
  """  Ensenya los resultados del escaner en forma de grafo con centro en IPV"""
  nodecolors=list(nodecolor_from_delay(delays,IPV))
  ls_nombres=list(delays.ip.values)
  G=nx.Graph()
  for i in range(0,len(ls_nombres)):
   # G.add_node(i, name=ls_nombres[i])
    G.add_node(i,color=nodecolors[i])
    
  labels={}
  for i in range(0,len(ls_nombres)):
    name=ls_nombres[i]
    labels[i]=name  
  G=nx.relabel_nodes(G,labels)
  for i in range(0,len(ls_nombres)):
    G.add_edge(IPV,ls_nombres[i])
  #print ["blue"]+list(nodecolor_from_delay(delays)),ls_nombres
  
  plt.figure(figsize=(15,15))  
  return G,nx.draw_graphviz(G,with_labels=True,node_color=[G.node[nod]['color'] for nod in G.nodes_iter()])

def nodecolor_from_delay(delays,source):
    colors= delays['alive'].map(aux).values
    colors[(delays.ip==source).values]='blue'
    #print colors,delays.ip.values
    return colors

def aux(x):
     
    if x:
        return "green"
    else:
        return "red"
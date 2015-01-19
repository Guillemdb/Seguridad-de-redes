import ScannerTemplates as st
import ScannerResults as sr
import Delays as dl
import ScanGraph as sg
import networkx as nx
from matplotlib import pyplot as plt  

class Scanner(object):
    def __init__(self,lips=None,lports=None):
        self.ip_list=lips
        self.port_list=lports
        self.results=None
        self.resources=None
        self.G=None
        self.colors=None
        
    def resources_from_localhost(self,payload="/"):
        """Escanea desde el propio ordenador la lista de puertos y hosts del scanner"""
        return st.scan_resources(self.ip_list,self.port_list)
    
    def dump_html(self,payload='/',filename='trap.html'):
        """Crea una pagina html que al visitarla activara el escaner de recursos"""
        return st.create_html(lips=self.ip_list,lports=self.port_list,payload=payload,filename=filename)
    
    def load_results(self,lips=None,lports=None):
        """Carga los resultados del escaneo realizado"""
        if not lips:
            lips=self.ip_list
        if not lports:
            lports=self.port_list            
        self.results=sr.load_results(lips,lports)
        return self.results
    
    def load_delays(self,classifier=None):
      """Carga los resultados procesados del escaner"""  
      if type(self.results)==None:
        self.results=self.load_results()
        self.resources=dl.df_resource_delays_from_result(self.results,classifier)
      else:  
        self.resources=dl.df_resource_delays_from_result(self.results,classifier)
      return self.resources
    
    def get_graph(self,IPV='0.0.0.0',node_atr='min',edge_atr='std'):
        
      nodecolors=sg.nodecolor_from_delay(self.resources,IPV)
      ls_nombres=self.resources.ip.values
      G=nx.Graph()
      """  
      labels={}
      for i in range(0,len(ls_nombres)):
        name=ls_nombres[i]
        labels[i]=name    
      """  
      for i in range(0,len(ls_nombres)):
      # G.add_node(i, name=ls_nombres[i])
        G.add_node(ls_nombres[i],color=nodecolors[i],atr=self.resources[node_atr].values[i])
      """ 
       labels={}
       for i in range(0,len(ls_nombres)):
        name=ls_nombres[i]
        labels[i]=name  
       G=nx.relabel_nodes(G,labels)
      """ 
      for i in range(0,len(ls_nombres)):
        if IPV!=ls_nombres[i]:    
         G.add_edge(IPV,ls_nombres[i],atr=self.resources[edge_atr].values[i])
        
      self.G=G
      self.colors=nodecolors
      return G,nodecolors
        
    def show_map(self,G=None,IPV='192.168.110.26',cmap=plt.cm.Greens):
       """  Ensenya los resultados del escaner en forma de grafo con centro en IPV y retorna el grafo de red"""
       if not G:
          if not self.G:
           self.G=self.get_graph(IPV)
          else:
           G=self.G
       else:
          pass             
       #print ["blue"]+list(nodecolor_from_delay(delays)),ls_nombres
       plt.figure(figsize=(20,15))  
       return G,nx.draw_graphviz(G,with_labels=True,node_color=[G.node[nod]['atr'] for nod in G.nodes_iter()],cmap=cmap,node_size=1500)
                
    def network_range(self,net,start,end):
      lips=[]
      for i in range(end-start):
        ipnum=self.ip_to_ints(net)
        ad=str(ipnum[0])+'.'+str(ipnum[1])+'.'+ str(ipnum[2])+'.'+str(start+i)
        lips.append(ad)
      self.ip_list=lips    
      return lips   
    
    def ip_to_ints(self,ip):
      return [int(x) for x in ip.split('.')]
import ScannerTemplates as st
import ScannerResults as sr
import Delays as dl
import ScanGraph as sg
import networkx as nx
from matplotlib import pyplot as plt 
import pickle
def network_range(net,start,end):
      lips=[]
      for i in range(end-start):
        ipnum=ip_to_ints(net)
        ad=str(ipnum[0])+'.'+str(ipnum[1])+'.'+ str(ipnum[2])+'.'+str(start+i)
        lips.append(ad)   
      return lips
    
def ip_to_ints(ip):
      return [int(x) for x in ip.split('.')]
def orden_from_ip(df):
    ips=df.index.values
    nums=[]
    for ip in ips:
        ips=ip.split('.')
        nums.append(int(ips[-1]))
    return nums

def orden_from_ip_res(df):
    ips=df.address.values
    nums=[]
    for ip in ips:
        ips=ip.split('.')
        nums.append(int(ips[-1]))
    return nums

def sort_delays_by_ip(df0):
    df=df0.copy()
    numip=orden_from_ip(df)
    df['num_ip']=numip
    df=df.sort('num_ip',ascending=True)
    return df

def sort_results_by_ip(df0):
    df=df0.copy()
    numip=orden_from_ip_res(df)
    df['num_ip']=numip
    df=df.sort('num_ip',ascending=True)
    return df

    
class ZreqScanner(object):
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
    
    def load_delays(self,classifier=None,maxdelay=30000,mindelay=3000):
      """Carga los resultados procesados del escaner"""  
      if type(self.results)==type(None):
        self.results=self.load_results()
        self.resources=dl.df_resource_delays_from_result(self.results,classifier,maxdelay,mindelay)
      else:  
        self.resources=dl.df_resource_delays_from_result(self.results,classifier,maxdelay,mindelay)
      return self.resources
    
    def get_graph(self,IPV='0.0.0.0',node_atr='min',edge_atr='std',data=None):
      if type(data)==type(None):
            data=self.resources
      nodecolors=sg.nodecolor_from_delay(data,IPV)
      ls_nombres=data.ip.values
      G=nx.Graph()
      """  
      labels={}
      for i in range(0,len(ls_nombres)):
        name=ls_nombres[i]
        labels[i]=name    
      """  
      for i in range(0,len(ls_nombres)):
      # G.add_node(i, name=ls_nombres[i])
        G.add_node(ls_nombres[i],color=nodecolors[i],atr=data[node_atr].values[i])
      """ 
       labels={}
       for i in range(0,len(ls_nombres)):
        name=ls_nombres[i]
        labels[i]=name  
       G=nx.relabel_nodes(G,labels)
      """ 
      for i in range(0,len(ls_nombres)):
        if IPV!=ls_nombres[i]:    
         G.add_edge(IPV,ls_nombres[i],atr=data[edge_atr].values[i])
        
      self.G=G
      self.colors=nodecolors
      return G,nodecolors
        
    def show_map(self,G=None,IPV='192.168.110.26',cmap=plt.cm.Greens,figsize=(20,15)):
       """  Ensenya los resultados del escaner en forma de grafo con centro en IPV y retorna el grafo de red"""
       if not G:
          if not self.G:
           self.G=self.get_graph(IPV)
          else:
           G=self.G
       else:
          pass             
       #print ["blue"]+list(nodecolor_from_delay(delays)),ls_nombres
       plt.figure(figsize=figsize)  
       return G,nx.draw_graphviz(G,with_labels=True,node_color=[G.node[nod]['atr'] for nod in G.nodes_iter()],cmap=cmap,node_size=1500)
                
    def show_alive(self,IPV='192.168.1.1',cmap=plt.cm.Greens,figsize=(20,15)):
       """  Ensenya los resultados del escaner en forma de grafo con centro en IPV y retorna el grafo de red"""
       filtered=self.resources[self.resources['alive']==True]
       G,colors=self.get_graph(IPV,data=filtered,node_atr='alive') 
       #print ["blue"]+list(nodecolor_from_delay(delays)),ls_nombres
       plt.figure(figsize=figsize)  
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
    
    def save_data(self,filename='scandata'):
        with open('res_'+filename, 'wb') as handle:
          pickle.dump(self.results, handle)
        with open('delays_'+filename, 'wb') as handle:
          pickle.dump(self.resources, handle)    
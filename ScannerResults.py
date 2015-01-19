import numpy as np
import pandas as pd
from pymongo import MongoClient

def load_results(lips,lports):
  """carga los resultados del scanner de la base de datos"""  
  ql=query_list(lips,lports)
  dl=retreive_resources(ql)
  return dict_list_to_df(dl)

def make_query(ip,port):
    """retorna un string en formato xxx.xxx.xxx.xxx:pppp. Servira para identificar elementos en el DataFrame"""
    return ip+':'+str(port)

def query_list(lips,lports):
    """obtiene los strings formateados como indices de la lista de ips i puertos pasada como parametro"""
    querys=[]
    for ip in lips:
        for port in lports:
            querys.append(make_query(ip,port))
    return querys

def retreive_resources(ql):
    """Aplica resource_from_id a la lista de querys pasadas por parametro"""
    return [resource_from_id(q) for q in ql]

def resource_from_id(s):
  """carga de la base de datos la query correspondiente guardada por el servidor"""  
  client = MongoClient('mongodb://localhost:27017/')
  db = client.scans
  collection = db.ips
  posts = db.ips
  di=posts.find_one({"ip_id": s})
  if di==None:
    di=get_default_dict(s)    
  return di

def get_default_dict(s):
    """En caso de pedir a la base de datos una query no realizada anteriormente se devuelve el  
       diccionario de la query con el valor de delay igua a -1"""
    ip,port=address_from_str(s)
    return { 'address': ip,'port': port,'delay': "-1",'ip_id':s}

def address_from_str(s):
    """A partir de una query retorna el numero de ip y de puerto"""
    return s.split(':')[0],s.split(':')[1]

def dict_list_to_df(dl):
    """dl: lista de diccionario obtenidos de la base de datos.
    convierte la lista en DataFrames para poder ser utilizada mas facilmente"""
    df=ip_dict_to_df(dl[0])
    for i in range(1,len(dl)):
        df=df.combine_first(ip_dict_to_df(dl[i]))
    return df 

def ip_dict_to_df(di):
    """Convierte un diccionario en un DataFrame con los mismos campos y valores"""
    #print di
    ip=pd.DataFrame(index=[di['ip_id']],columns=['address','port','delay'])
    ip.address=di['address']
    ip.port=di['port']
    ip.delay=int(di['delay'])
    return ip
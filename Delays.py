import numpy as np
import pandas as pd


def df_resource_delays_from_result(sr,classifier,maxdelay,mindelay):
    """Obtiene un DataFrame que contiene la informacion del escaner procesada"""
    mi,ma,std,mean=ip_delays_from_results(sr)
    delays=ip_delay(mi[0],ma[0],std[0],mean[0],classifier)
    for i in range(1,len(mi)):
        delays=delays.combine_first(ip_delay(mi[i],ma[i],std[i],mean[i],classifier,maxdelay,mindelay))
    return delays 

def ips_from_results(sr):
    """sr: DataFrame que contiene los resultados de un escaneo
       retorna una lista que contiene las ips de las que hemos obtenido respuesta en el escaner"""
    return list(set(sr[sr.delay>0].address))

def ip_delays_from_results(sr):
    """Obtiene las diferentes metricas derivadas de los retardos"""
    return [sr[sr.delay>0][sr.address==ip].min() for ip in ips_from_results(sr)],[sr[sr.delay>0][sr.address==ip].max() for ip in ips_from_results(sr)],[sr[sr.delay>0][sr.address==ip].std() for ip in ips_from_results(sr)],[sr[sr.delay>0][sr.address==ip].mean() for ip in ips_from_results(sr)]

def ip_delay(mi,ma,std,mean,classifier=None,maxdelay=30000,mindelay=3000):
    """con las metricas derivadas del delay determina si el recurso esta disponible o no"""  
    delays=pd.DataFrame(index=[mi.address],columns=['ip','max','min','mean','std','alive'])
    delays.ip=mi.address
    delays['max']=ma.delay
    delays['min']=mi.delay
    delays['mean']=mean.delay  
    delays['std']=std.delay  
    delays['mdmax']=delays['min']/delays['max']
    delays['maxdm']=delays['max']/delays['min']  
    delays['maxsm']=delays['max']-delays['min'] 
    if classifier:  
      delays['alive']=classify_delay(delays,classifier)  #AI
    else:      
      delays['alive']=False  
      if delays['max'].values>maxdelay:
        delays['alive']=True
      elif delays['min'].values<mindelay:
          delays['alive']=True    
    return delays  
def classify_delay(delays,classifier):
    X=delays.drop(['ip','alive'],axis=1)
    #print "pred",clf.predict(X)
    return classifier.predict(X)
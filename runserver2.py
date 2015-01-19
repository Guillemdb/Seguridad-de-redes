from eve import Eve
from pymongo import MongoClient
#app = Eve()

def list_to_ip(l):
    return str(l[0])+'.'+str(l[1])+'.'+str(l[2])+'.'+str(l[3])

def string_to_ip(s):
    #print "s in ip",s
    splited=s.split('x')
    port=int(splited[1])
    #print"port", port
    ipl=splited[0].split('o')
    #print "address",ipl
    address=list_to_ip(ipl)
    ip_id=str(address)+':'+str(port)
    
    delay=str(splited[2])
    print"results:",ip_id, delay
    ip={ 'address': address,'port': port,'delay': delay,'ip_id':ip_id}
    return ip

def ip_dict_to_df(di):
    ip=pd.DataFrame(index=[di['ip_id']],columns=['address','port','delay'])
    ip.address=di['address']
    ip.port=di['port']
    ip.delay=di['delay']
    return ip

#from eve import Eve




def pre_get_callback(resource, request, lookup):
    #print 'A GET request on the "%s" endpoint has just been received!' % resource
    print  'REQ %s ' % request
    from pymongo import MongoClient
    ifirst=str(request)
    #print "FIRST",ifirst
    sec=str(ifirst)[len("<Request 'http://127.0.0.1:5000/ips/")::]
    #print "SEC: ",sec
    ids=sec[:-len("' [GET]>")]
    #print "ids:",ids
    ipsample=string_to_ip(ids)
    #print "ip_id",ipsample
    client = MongoClient('mongodb://localhost:27017/')
    db = client.apitest
    collection = db.ips
    posts = db.ips
    post_id = posts.insert(ipsample)
    print "Added to db"
    print post_id
    
    
def pre_contacts_get_callback(request, lookup):
    print 'A GET request on the contacts endpoint has just been received in: %s!' %resource
    print "miaus"
    """
    ipsample=string_to_ip(str(resource)[5:])
    print "ip_id",ipsample

    client = MongoClient('mongodb://localhost:27017/')
    db = client.apitest
    collection = db.ips
    posts = db.ips
    post_id = posts.insert(ipsample)
    print "done"  """  

app = Eve()


#app.run()
if __name__ == '__main__':
 
  app.on_pre_GET += pre_get_callback
  app.on_pre_GET_contacts += pre_contacts_get_callback  
  app.run()  
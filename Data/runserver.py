from eve import Eve
from pymongo import MongoClient
#app = Eve()
def string_to_ip(s):
    splited=s.split('x')
    port=int(splited[1])
    ipl=splited[0].split('o')
    address=list_to_ip(ipl)
    state=str(splited[2])
    ip={ 'address': address,'port': port,'state': state,'ip_id':s}
    return ip


#from eve import Eve




def pre_get_callback(resource, request, lookup):
    print 'A GET request on the "%s" endpoint has just been received!' % resource
    ipsample=string_to_ip(str(resource)[5:])
    print "ip_id",ipsample
    client = MongoClient('mongodb://localhost:27017/')
    db = client.apitest
    collection = db.ips
    posts = db.ips
    post_id = posts.insert(ipsample)
    print post_id
    
    
def pre_contacts_get_callback(request, lookup):
    #print 'A GET request on the contacts endpoint has just been received!'
    
    ipsample=string_to_ip(str(resource)[5:])
    print "ip_id",ipsample

    client = MongoClient('mongodb://localhost:27017/')
    db = client.apitest
    collection = db.ips
    posts = db.ips
    post_id = posts.insert(ipsample)
    print "done"    

app = Eve()

app.on_pre_GET += pre_get_callback
app.on_pre_GET_contacts += pre_contacts_get_callback
#app.run()
if __name__ == '__main__':
  app.run()
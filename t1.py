#Prereq: pyyaml libs and pyzabbix libs

from pyzabbix import ZabbixAPI
import yaml
# Zabbix url, zabbix username and password
url = 'http://zobbegz'
zuser = 'Admin'
zpassword = 'zabbix'
yfilepath = 'D:\\data.yaml'
#Loading file (if exists)
try:
   with open(yfilepath) as f:
    
    docs = yaml.load_all(f, Loader=yaml.FullLoader)
    for doc in docs:
# Gathering hosts, hostgroup, templates from file. Dirty code, won't work for more than one section in yaml        
           for k, v in doc.items():
               if k == 'hosts_list':
                  rhosts = v
               elif k == 'hostgroup':
                  rhostgroupname = v
               elif k == 'templates_list':
                  rtempllist = v
except FileNotFoundError:
	print("File not found")
else:
#Connecting to server, gathering data for hosts and groups
   z = ZabbixAPI(url, user=zuser, password=zpassword)
   groups = z.hostgroup.get(output=['name'])
   hosts = z.host.get(output=['name'])
   flag = 0
   for j in groups:
# Checking if the hostgroup already exists
       if j['name'] == rhostgroupname:
           exgroupid = j['groupid']
           flag = 1
#Creating group if none found
   if flag == 0:
     exgroupid = z.hostgroup.create({'name':rhostgroupname})['groupids']
   extplid=[]
#Collecting template list from server, getting templateid's. Assumed templates are already there (or it will last till next friday))
   templates = z.template.get(output=['name'])
   for i in rtempllist:
     for j in templates:
             if j['name'] == i:
                 extplid.append(j['templateid'])

#Getting names of the hosts, already exist on server
   k=[]
   for m in hosts:
      k.append(m['name'])
   zhosts = k
   
#Creating new hosts, if any
   for rhost in rhosts:
	   if rhost not in zhosts:
		   d = {'host':rhost,'interfaces':[{'type':1,'main':1,'useip':1,'ip':'127.0.0.2','dns':'','port':'10050'}],'groups':[{'groupid':exgroupid}],'templates':extplid}
		   z.host.create(d)
	   else:
		   print(rhost, "is in") 
	   
   



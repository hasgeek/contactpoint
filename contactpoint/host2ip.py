import threading
import time
import socket
from os import environ

def host2ip(f):
    def host2ipf(*a, **kw):
        try:
            t = threading.Thread(target=f,args=a,kwargs=kw)
            t.daemon = True
            t.start()
        except (KeyboardInterrupt, SystemExit):
            print '\nApplication over'
    return host2ipf

@host2ip
def start_host2ip(CP):
    if len(environ['REMOTE_SERVERS']) == 0:
        return
    hostname = environ['PEOPLEFLOW_HOSTNAME']
    t = environ['HOST2IP_PERIOD']
    CP.logger.log('Resolving ' + hostname)
    server_ip = None
    def resolve(CP, hostname, server_ip):
        try:
            ip = socket.gethostbyname(hostname)
            CP.logger.log("IP is " + ip)
        except:
            CP.logger.log("Unable to resolve")
            ip = None
        if ip != server_ip and ip is not None:
            CP.logger.log("IP Changed")
            hosts = open('/etc/hosts','r+')
            servers = environ['REMOTE_SERVERS']
            lines = {}
            for line in hosts:
                map = line.split()
                update = False
                pops = []
                for server in servers:
                    if server in map or (server + ',') in map:
                        CP.logger.log(server + ' exists')
                        if map[0] != ip:
                            CP.logger.log(server + " is not set to " + ip)
                            update = True
                        else:
                            CP.logger.log(server + " is already set to " + ip)
                        pops.append(server)
                for pop in pops:
                    servers.pop(servers.index(pop))
                if update:
                    lines[line] = line.replace(map[0], ip)
            hosts.close()
            if len(lines):
                with open("/etc/hosts", 'r') as f:
                    hosts = f.read()
                    f.close()
                for line in lines:
                    CP.logger.log(("Updating " + line + " -> " + lines[line]).replace('\n',''))
                    hosts = hosts.replace(line, lines[line])
                with open("/etc/hosts", 'w') as f:
                    f.write(hosts)
                    f.close()

            if len(servers):
                hosts = open("/etc/hosts", 'a')
                for server in servers:
                    CP.logger.log(server + " doesnt exist")
                    new = "\n" + ip + " " + server
                    CP.logger.log("Writing " + new)
                    hosts.write(new)
                hosts.close()
        return ip


    while True:
        time.sleep(t)
        server_ip = resolve(CP, hostname, server_ip)

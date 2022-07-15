import docker
import socket

client = docker.from_env()

def CheckIfPortIsAvailableOnOS(port):    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('localhost', port))
        s.shutdown(2)
        return False
    except:
        return True

def RunContainer(imagename,imageport,labport):
    try:
        client.images.pull(imagename)
    except:
        return {'error':'Image not found or not publically available'}
    try:
        if (CheckIfPortIsAvailableOnOS(imageport)):
            container = client.containers.run(imagename,detach=True,ports={imageport:labport})
            return {'success':'Container Created and Running','id':container.short_id}
        else:
            return {'error':'Port already in use'}
    except Exception as e:
        return {'error':e}
     
def ShowRunningContainers():
    containers = client.containers.list()
    containers_lst = []
    for container in containers:
        containers_lst.append({"name":container.name,"id":container.short_id,"image":container.image.tags[0],"ports":container.ports,"status":container.status,"ip":container.attrs['NetworkSettings']['Networks']['bridge']['IPAddress'],"time":container.attrs['State']['StartedAt'],"hostport":getHostPort(container.attrs['NetworkSettings']['Ports'])})
    return containers_lst

def getHostPort(ports):
    try:    
        for key, value in ports.items():
            for item in value:
                return item['HostPort']
    except:
        return None        

def KillContainer(containerid):
    protectedImages = ['ghcr.io/adgsenpai/adglab','ghcr.io/adgsenpai/httpwebos']
    try:
        container = client.containers.get(containerid)
        if container.image.tags[0] in protectedImages:
            return {'error':'Container is protected'}
        else:
            container.stop()
            container.remove()
            return {'status':'Container killed','id':containerid}
    except:
        return {'error':'Container not found'}
from mininet.net import Mininet
from mininet.net import Containernet, OVSKernelSwitch
from mininet.node import Controller
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

#create our network
net = Containernet(controller=RemoteController, switch=OVSKernelSwitch)
info('*** Adding controller\n')
#create our controllers
c1 =net.addController('c1',Controller=RemoteController,port=6655,ip='127.0.0.1')
c2 =net.addController('c2',Controller=RemoteController,port=6633)


info('*** Adding docker containers\n')
#create our Docker containers
#note the dimage is set specific to my set up, change to your local docker image
host1 = net.addDocker('host1', ip='192.168.2.10',dimage="ubuntu:nmap",mac='00:00:00:00:00:02')
host2 = net.addDocker('host2', ip='192.168.2.20',dimage="ubuntu:nmap",mac='00:00:00:00:00:01')
host3 = net.addDocker('host3', ip='192.168.2.30',dimage="ubuntu:nmap",mac='00:00:00:00:00:03')
host4 = net.addDocker('host4', ip='192.168.2.40',dimage="ubuntu:nmap",mac='00:00:00:00:00:04')



info('*** Adding switches\n')
#create switch
s1 = net.addSwitch('s1')
#link our hosts, switch, and controller together
info('*** Creating links\n')
net.addLink(c2,s1)
net.addLink(s1,host1)
net.addLink(s1,host2)
net.addLink(s1,host3)
net.addLink(s1,host4)



info('*** Testing connectivity\n')
#start the network
s1.start([c1,c2])
net.start()
#optional communication test
net.ping([host1,host2])
net.ping([host2,host3])
net.ping([host3,host4])
#start CLI
CLI(net)
#stop our network
info('*** Stopping network')
net.stop()


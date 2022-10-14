#!/usr/bin/env python
import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi

def topology(args):
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8' )
    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8', range='20' )
    ap1 = net.addAccessPoint( 'ap1', ssid= 'link1', mode= 'g', channel= '1', position='30,75,0', range='20' )
    ap2 = net.addAccessPoint( 'ap2', ssid= 'link2', mode= 'g', channel= '1', position='60,100,0', range='20' )
    ap3 = net.addAccessPoint( 'ap3', ssid= 'link3', mode= 'g', channel= '1', position='100,100,0', range='20' )
    ap4 = net.addAccessPoint( 'ap4', ssid= 'link4', mode= 'g', channel= '1', position='130,75,0', range='20' )
    ap5 = net.addAccessPoint( 'ap5', ssid= 'link5', mode= 'g', channel= '1', position='100,50,0', range='20' )
    ap6 = net.addAccessPoint( 'ap6', ssid= 'link6', mode= 'g', channel= '1', position='60,50,0', range='20' )
    c1 = net.addController('c1')

    info("*** Configuring Propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.addLink(ap1, h1)
    net.addLink(ap1, ap2)
    net.addLink(ap2, ap3)
    net.addLink(ap3, ap4)
    net.addLink(ap4, ap5)
    net.addLink(ap5, ap6)
    net.addLink(ap1, ap6)

    if '-p' not in args:
        net.plotGraph(max_x=140, max_y=140)

    net.startMobility(time=0, ac_method='ssf')
    net.mobility(sta1, 'start', time=10, position='1,75,0')
    net.mobility(sta1, 'stop', time=70, position='140,75,0')
    net.stopMobility(time=80)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])
    ap5.start([c1])
    ap6.start([c1])

    info("*** Running CLI\n")
    CLI( net )

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology(sys.argv)

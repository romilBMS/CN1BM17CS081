# -*-  Mode: Python; -*-
# /*
#  * This program is free software; you can redistribute it and/or modify
#  * it under the terms of the GNU General Public License version 2 as
#  * published by the Free Software Foundation;
#  *
#  * This program is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  * GNU General Public License for more details.
#  *
#  * You should have received a copy of the GNU General Public License
#  * along with this program; if not, write to the Free Software
#  * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#  *
#  * Ported to Python by Mohit P. Tahiliani
#  */

import ns.core
import ns.network
import ns.csma
import ns.internet
import ns.point_to_point
import ns.applications
import sys

# // Default Network Topology
# //
# //       10.1.1.0
# // n0 -------------- n1   n2   n3   n4 (-------- n5)
# //    point-to-point  |    |    |    |     p2p
# //                    ================
# //                      LAN 10.1.2.0

'''
    changes made: 
                add n5 as client , and connect to n5 P2P(5Mbps, 5ms)
                n3 is the server 
                n0 and n5 client
'''

cmd = ns.core.CommandLine()
cmd.nCsma = 2 #was 3
cmd.verbose = "True"
cmd.AddValue("nCsma", "Number of \"extra\" CSMA nodes/devices")
cmd.AddValue("verbose", "Tell echo applications to log if true")
cmd.Parse(sys.argv)

nCsma = int(cmd.nCsma)
verbose = cmd.verbose

if verbose == "True":
	ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
	ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)
nCsma = 1 if int(nCsma) == 0 else int(nCsma)

p2pNodes = ns.network.NodeContainer()
p2pNodes.Create(2) 

p2pNodes2 = ns.network.NodeContainer() #/e
p2pNodes2.Create(2) #\e

csmaNodes = ns.network.NodeContainer()
csmaNodes.Add(p2pNodes.Get(1))
csmaNodes.Add(p2pNodes2.Get(0)) #e
csmaNodes.Create(nCsma)

pointToPoint = ns.point_to_point.PointToPointHelper()
pointToPoint.SetDeviceAttribute("DataRate", ns.core.StringValue("5Mbps"))
pointToPoint.SetChannelAttribute("Delay", ns.core.StringValue("2ms"))

p2pDevices = pointToPoint.Install(p2pNodes)
p2pDevices2= pointToPoint.Install(p2pNodes2) #ex

csma = ns.csma.CsmaHelper()
csma.SetChannelAttribute("DataRate", ns.core.StringValue("100Mbps"))
csma.SetChannelAttribute("Delay", ns.core.TimeValue(ns.core.NanoSeconds(6560)))

csmaDevices = csma.Install(csmaNodes)

stack = ns.internet.InternetStackHelper()
stack.Install(p2pNodes.Get(0))
stack.Install(csmaNodes)
stack.Install(p2pNodes2.Get(1)) #e


address = ns.internet.Ipv4AddressHelper()
address.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
p2pInterfaces = address.Assign(p2pDevices)

address.SetBase(ns.network.Ipv4Address("10.1.2.0"), ns.network.Ipv4Mask("255.255.255.0"))
csmaInterfaces = address.Assign(csmaDevices)

address.SetBase(ns.network.Ipv4Address("10.1.3.0"), ns.network.Ipv4Mask("255.255.255.0")) #e
p2pInterfaces2 = address.Assign(p2pDevices2) #e

echoServer = ns.applications.UdpEchoServerHelper(9)

serverApps = echoServer.Install(csmaNodes.Get(nCsma))
serverApps.Start(ns.core.Seconds(1.0))
serverApps.Stop(ns.core.Seconds(10.0))

echoClient = ns.applications.UdpEchoClientHelper(csmaInterfaces.GetAddress(nCsma), 9)
echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds (1.0)))
echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

clientApps = echoClient.Install(p2pNodes.Get(0))
clientApps.Start(ns.core.Seconds(2.0))
clientApps.Stop(ns.core.Seconds(10.0))

clientApps2 = echoClient.Install(p2pNodes2.Get(1))#e
clientApps2.Start(ns.core.Seconds(3.0))#e
clientApps2.Stop(ns.core.Seconds(10.0))#e

ns.internet.Ipv4GlobalRoutingHelper.PopulateRoutingTables()

pointToPoint.EnablePcapAll("second")
csma.EnablePcap ("second", csmaDevices.Get (1), True)

ns.core.Simulator.Run()
ns.core.Simulator.Destroy()


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
#  */

# import ns.applications
# import ns.core
# import ns.internet
# import ns.network
# import ns.point_to_point

# ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
# ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

# nodes = ns.network.NodeContainer()
# nodes.Create(3)# /*
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
#  */

import ns.applications
import ns.core
import ns.internet
import ns.network
import ns.point_to_point
import ns.applications
import ns.core
import ns.internet
import ns.network
import ns.point_to_point

ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

nodes = ns.network.NodeContainer()
nodes.Create(2)



ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

nodes = ns.network.NodeContainer()
nodes.Create(3) #3

pointToPoint = ns.point_to_point.PointToPointHelper()
pointToPoint.SetDeviceAttribute("DataRate", ns.core.StringValue("5Mbps"))
pointToPoint.SetChannelAttribute("Delay", ns.core.StringValue("2ms"))

devices = pointToPoint.Install(nodes.Get(0), nodes.Get(1)) #install p2p on device 1 and server 
devices2 = pointToPoint.Install(nodes.Get(1), nodes.Get(2)) #install p2p on device 2 and server

stack = ns.internet.InternetStackHelper()
stack.Install(nodes)

address = ns.internet.Ipv4AddressHelper()
address.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
address2 = ns.internet.Ipv4AddressHelper() #change
address2.SetBase(ns.network.Ipv4Address("10.1.2.0"),ns.network.Ipv4Mask("255.255.255.0"))


interfaces = address.Assign(devices)
interfaces2 = address2.Assign(devices2) #p2p interface for 2nd set

echoServer = ns.applications.UdpEchoServerHelper(9)

serverApps = echoServer.Install(nodes.Get(1))
serverApps.Start(ns.core.Seconds(1.0))
serverApps.Stop(ns.core.Seconds(10.0))

#make 1st node as 1st client

echoClient = ns.applications.UdpEchoClientHelper(interfaces.GetAddress(1), 9)
echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(1.0)))
echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

clientApps= echoClient.Install(nodes.Get(0))
clientApps.Start(ns.core.Seconds(2.0))
clientApps.Stop(ns.core.Seconds(10.0))

#make 3rd as the 2nd client

echoClient2 = ns.applications.UdpEchoClientHelper(interfaces2.GetAddress(0), 9)
echoClient2.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
echoClient2.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(1.0)))
echoClient2.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

clientApps= echoClient.Install(nodes.Get(2))
clientApps.Start(ns.core.Seconds(2.0))
clientApps.Stop(ns.core.Seconds(10.0))        

ns.core.Simulator.Run()
ns.core.Simulator.Destroy()



# pointToPoint = ns.point_to_point.PointToPointHelper()
# pointToPoint.SetDeviceAttribute("DataRate", ns.core.StringValue("5Mbps"))
# pointToPoint.SetChannelAttribute("Delay", ns.core.StringValue("2ms"))

# devices = pointToPoint.Install(nodes)

# stack = ns.internet.InternetStackHelper()
# stack.Install(nodes)

# address = ns.internet.Ipv4AddressHelper()
# address.SetBase(ns.network.Ipv4Address("10.1.1.0"),
#                 ns.network.Ipv4Mask("255.255.255.0"))

# interfaces = address.Assign(devices)

# echoServer = ns.applications.UdpEchoServerHelper(9)

# serverApps = echoServer.Install(nodes.Get(1))
# serverApps.Start(ns.core.Seconds(1.0))
# serverApps.Stop(ns.core.Seconds(10.0))

# echoClient = ns.applications.UdpEchoClientHelper(interfaces.GetAddress(1), 9)
# echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
# echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(1.0)))
# echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

# clientApps = echoClient.Install(nodes.Get(0))
# clientApps.Start(ns.core.Seconds(2.0))
# clientApps.Stop(ns.core.Seconds(10.0))

# ns.core.Simulator.Run()
# ns.core.Simulator.Destroy()

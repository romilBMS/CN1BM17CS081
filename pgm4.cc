#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/netanim-module.h"
#include "ns3/mobility-module.h"
#include "ns3/animation-interface.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("NS3ScriptExample");

int main (int argc, char *argv[])
{
  bool verbose=true;
  uint32_t nCsma=3,np2p=2;
  
  CommandLine cmd;
  cmd.AddValue("nCsma","Number of \"extra\"CSMA naades/devices",nCsma);
  cmd.AddValue("verbose","Tell echo applications to log if true",verbose);
  
  cmd.Parse(argc,argv);
  
  if(verbose)
  {
  LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
  LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);
  }
  
  nCsma=nCsma==0?1:nCsma;
  
  NodeContainer p2pn;
  p2pn.Create(np2p);
  
  NodeContainer csman;
  csman.Add(p2pn.Get(1));
  csman.Create(nCsma);
  
  PointToPointHelper ptp;
  ptp.SetDeviceAttribute("DataRate",StringValue("5Mbps"));
  ptp.SetChannelAttribute("Delay",StringValue("2ms"));
  
  NetDeviceContainer p2pd;
  p2pd=ptp.Install(p2pn);
  
  CsmaHelper csma;
  csma.SetChannelAttribute("DataRate",StringValue("100Mbps"));
  csma.SetChannelAttribute("Delay",TimeValue(NanoSeconds(6560)));
  
  NetDeviceContainer csmad;
  csmad=csma.Install(csman);
  
  InternetStackHelper st;
  st.Install(p2pn.Get(0));
  st.Install(csman);
  
  Ipv4AddressHelper address;
  address.SetBase("10.1.1.0","255.255.255.0");
  
  Ipv4InterfaceContainer p2pInterfaces;
  p2pInterfaces=address.Assign(p2pd);
  
  address.SetBase("10.1.2.0","255.255.255.0");
  
  Ipv4InterfaceContainer csmaInterfaces;
  csmaInterfaces=address.Assign(csmad);
  
  UdpEchoServerHelper echoServer(9);
  
  ApplicationContainer serverApps=echoServer.Install(csman.Get(nCsma));
  serverApps.Start(Seconds(1.0));
  serverApps.Stop(Seconds(10.0));
  
  UdpEchoClientHelper echoClient(csmaInterfaces.GetAddress(nCsma),9);
  echoClient.SetAttribute("MaxPackets",UintegerValue(1));
  echoClient.SetAttribute("Interval",TimeValue(Seconds(1.0)));
  echoClient.SetAttribute("PacketSize",UintegerValue(1024));
  
  ApplicationContainer clientApps=echoClient.Install(p2pn.Get(0));
  clientApps.Start(Seconds(2.0));
  clientApps.Stop(Seconds(10.0));
  
  Ipv4GlobalRoutingHelper::PopulateRoutingTables();
  
  ptp.EnablePcapAll("second");
  csma.EnablePcap("second",csmad.Get(1),true);
  
  AnimationInterface anim("anim_sec.xml");
  
  anim.SetConstantPosition(p2pn.Get(0),0.5,0.5);
  anim.SetConstantPosition(csman.Get(0),10.0,10.0);
  anim.SetConstantPosition(csman.Get(1),20.5,20.5);
  anim.SetConstantPosition(csman.Get(2),40.5,40.5);
  anim.SetConstantPosition(csman.Get(3),60.5,60.5);
  
  anim.EnablePacketMetadata(true);
  Simulator::Run();
  Simulator::Destroy();
  return 0;
  }


import ns3
import visualizer

#ns3.LogComponentEnable("OnOffApplication", ns3.LOG_LEVEL_ALL)
ns3.LogComponentEnable("PacketSink", ns3.LOG_LEVEL_ALL)
nodes = ns3.NodeContainer()
nodes.Create(3)

wifihelper = ns3.WifiHelper()
wifihelper.SetStandard(ns3.WIFI_PHY_STANDARD_80211b)
wifiphyhelper = ns3.YansWifiPhyHelper()
wifiphy = wifiphyhelper.Default()
wifiphy.Set("TxGain", ns3.DoubleValue(25))
wifiphy.Set("RxGain", ns3.DoubleValue(90))
wifichannel = ns3.YansWifiChannelHelper()
wifi_chan = wifichannel.Default()
wifi_chan.AddPropagationLoss("ns3::FriisPropagationLossModel")
wifiphy.SetChannel(wifi_chan.Create())

mac = ns3.NqosWifiMacHelper.Default()
mac.SetType("ns3::AdhocWifiMac")

wifihelper.SetRemoteStationManager("ns3::ConstantRateWifiManager", "DataMode", ns3.StringValue("DsssRate1Mbps"), "ControlMode", ns3.StringValue("DsssRate1Mbps"))
devices = wifihelper.Install(wifiphy,mac,nodes)

olsr = ns3.OlsrHelper()
    
#Add the IPv4 protocol stack to the nodes in our container
internet=ns3.InternetStackHelper()
internet.SetRoutingHelper (olsr)
 
internet.Install (nodes)
ipaddrss= ns3.Ipv4AddressHelper()
ipaddrss.SetBase(ns3.Ipv4Address("192.168.0.0"), ns3.Ipv4Mask("255.255.255.0"));
ipcontainer = ipaddrss.Assign(devices);
    
mobility = ns3.MobilityHelper()
positionAlloc = ns3.ListPositionAllocator()
positionAlloc.Add(ns3.Vector (100,100,0.0))
positionAlloc.Add(ns3.Vector (100,200,0.0))    
positionAlloc.Add(ns3.Vector (200,200,0.0))    

mobility.SetPositionAllocator(positionAlloc)
mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
mobility.Install(nodes)

port = 5000

#On off Application

onoff = ns3.OnOffHelper("ns3::UdpSocketFactory", ns3.Address(ns3.InetSocketAddress(ipcontainer.GetAddress(1),port)))
onoff.SetAttribute("OnTime", ns3.RandomVariableValue(ns3.ConstantVariable(42)))
onoff.SetAttribute("OffTime", ns3.RandomVariableValue(ns3.ConstantVariable(0)))

#onoff.SetAttribute ("Remote", ns3.AddressValue (ns3.InetSocketAddress(ipcontainer.GetAddress(1),port)));
apps = onoff.Install(nodes.Get(0))

apps.Start(ns3.Seconds(0.1))
apps.Stop(ns3.Seconds(90.0))

sink = ns3.PacketSinkHelper("ns3::UdpSocketFactory", ns3.InetSocketAddress (ipcontainer.GetAddress (1), port))
appsink = sink.Install (nodes.Get (1))

appsink.Start(ns3.Seconds(0.5))
appsink.Stop(ns3.Seconds(90.0))
ns3.Simulator.Stop(ns3.Seconds(100))
#ns3.Simulator.Run()
visualizer.start()
ns3.Simulator.Destroy()

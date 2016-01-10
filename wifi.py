import ns3
nodes = ns3.NodeContainer()
nodes.Create(2)

wifihelper = ns3.WifiHelper()

wifiphyhelper = ns3.YansWifiPhyHelper()
wifiphy = wifiphyhelper.Default()
wifichannel = ns3.YansWifiChannelHelper()
wifi_chan = wifichannel.Default()
wifiphy.SetChannel(wifi_chan.Create())

mac = ns3.NqosWifiMacHelper.Default()
mac.SetType("ns3::AdhocWifiMac")

wifihelper.SetRemoteStationManager("ns3::ConstantRateWifiManager", "DataMode", ns3.StringValue("wifia-54mbs"))
wifihelper.Install(wifiphy,mac,nodes)


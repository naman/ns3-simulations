# Building a CSMA based network consisting of 4 nodes
import ns3

nodes = ns3.NodeContainer()

nodes.Create(4)

stack = ns3.InternetStackHelper()
stack.Install (nodes)

csma =ns3.CsmaHelper()
devices = csma.Install(nodes)

address = ns3.Ipv4AddressHelper()
address.SetBase(ns3.Ipv4Address("10.1.1.0"), ns3.Ipv4Mask("255.255.255.0"))
interfaces = address.Assign(devices)


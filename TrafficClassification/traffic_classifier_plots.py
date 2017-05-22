#!/usr/bin/env python

"""Traffic Analyser: classifies the traffic based on Protocols and plots a graph"""

__author__      = "Lakshmi Srinivas, Ashwin Kini, Subhdarshi Samal"

from scapy.all import *
import dpkt
import plotly.plotly as py
import plotly.graph_objs as go

#Run tcpdump and collect the packets into a pcap
#sudo tcpdump -ni ovsbr0 -s0 -w new.pcap

#Read packets fro pcap file
pkts = rdpcap('traffic.pcap')
tcpCounter = 0
udpCounter = 0
httpCounter = 0
sshCounter = 0
arpCounter = 0
icmpCounter = 0

#SSH Filters
ports = [22]
filtered_ssh = (pkt for pkt in pkts if
    TCP in pkt and
    (pkt[TCP].sport in ports or pkt[TCP].dport in ports))
wrpcap('filtered_ssh.pcap', filtered_ssh)	#copy ssh packets to pcap
for i in dpkt.pcap.Reader(open('filtered_ssh.pcap', 'r')):
	sshCounter+=1

#ICMP Filters
filtered_icmp = (pkt for pkt in pkts if
    ICMP in pkt)
wrpcap('filtered_icmp.pcap', filtered_icmp)	#copy ICMP packets to pcap
for i in dpkt.pcap.Reader(open('filtered_icmp.pcap', 'r')):
	icmpCounter+=1

#HTTP Filters
ports = [80, 443]
filtered_http = (pkt for pkt in pkts if
    TCP in pkt and
    (pkt[TCP].sport in ports or pkt[TCP].dport in ports))
wrpcap('filtered_http.pcap', filtered_http)	#copy http packets to pcap
for i in dpkt.pcap.Reader(open('filtered_http.pcap', 'r')):
	httpCounter+=1

#ARP Filters
filtered_arp = (pkt for pkt in pkts if
    ARP in pkt)
wrpcap('filtered_arp.pcap', filtered_arp)	#copy arp packets to pcap
for i in dpkt.pcap.Reader(open('filtered_arp.pcap', 'r')):
	arpCounter+=1

#TCP Filters
ports = [22, 80, 443]
filtered_tcp = (pkt for pkt in pkts if
    TCP in pkt and
    (pkt[TCP].sport not in ports or pkt[TCP].dport not in ports))
wrpcap('filtered_tcp.pcap', filtered_tcp)	#copy tcp packets to pcap
for i in dpkt.pcap.Reader(open('filtered_tcp.pcap', 'r')):
	tcpCounter+=1

#UDP Filters
filtered_udp = (pkt for pkt in pkts if
    UDP in pkt)
wrpcap('filtered_udp.pcap', filtered_udp)	#copy UDP packets to pcap
for i in dpkt.pcap.Reader(open('filtered_udp.pcap', 'r')):
	udpCounter+=1


data = [go.Bar(
            x=['arp', 'icmp', 'tcp', 'udp', 'ssh', 'http'],
            y=[arpCounter, icmpCounter, tcpCounter, udpCounter, sshCounter, httpCounter],
	    name='Traffic Classification',
	    marker=dict(
	        color='rgb(26, 118, 255)'
	    )
    )]

py.iplot(data, filename='asw-bar')


from __future__ import print_function
"""
Use DPKT to read in a pcap file and print out the contents of the packets
This example is focused on the fields in the Ethernet Frame and IP packet
"""
import dpkt
import datetime
import socket
from dpkt.compat import compat_ord
import binascii
import pymavlink
from pymavlink.dialects.v10 import ardupilotmega as apm
import json


def mac_addr(address):
    """Convert a MAC address to a readable/printable string

       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % compat_ord(b) for b in address)



def inet_to_str(inet):
    """Convert inet object to a string

        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    # First try ipv4 and then ipv6
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


def print_packets(pcap):
    """Print out information about each packet in a pcap

       Args:
           pcap: dpkt pcap reader object (dpkt.pcap.Reader)
    """

    total = []

    # For each packet in the pcap process the contents
    for timestamp, buf in pcap:

        # Print out the timestamp in UTC
        #print('Timestamp: ', str(datetime.datetime.fromtimestamp(timestamp)))

        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)
        #print('Ethernet Frame: ', mac_addr(eth.src), mac_addr(eth.dst), eth.type)

        # Make sure the Ethernet data contains an IP packet
        if not isinstance(eth.data, dpkt.ip.IP):
            #print('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__)
            continue

        # Now unpack the data within the Ethernet frame (the IP packet)
        # Pulling out src, dst, length, fragment info, TTL, and Protocol
        ip = eth.data

        # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
        do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
        more_fragments = bool(ip.off & dpkt.ip.IP_MF)
        fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

        # Print out the IP info
        #print('IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)' % \
        #      (inet_to_str(ip.src), inet_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset))

        # Extrack UDP data from IP datagram
        udp = ip.data
        #print('UDP: %d -> %d (ulen=%d sum=%d)' % (udp.sport, udp.dport, udp.ulen, udp.sum) )

        # Extrack MAVLINK data from UDP datagram
        mavlink_data        = udp.data
        mavlink_object      = apm.MAVLink(mavlink_data)
        mavlink_msg         = mavlink_object.parse_buffer(mavlink_data)[0]
        mavlink_msg_type    = mavlink_msg.get_type()

        #print("MAVLINK: %d bytes" %(len(mavlink_data)))
        #print("MSG: %s" %(mavlink_msg_type))
        #print(mavlink_msg)
        #print()

        data                    = {}
        data["Time"]            = timestamp
        data["IpSrc"]           = inet_to_str(ip.src)
        data["IpDst"]           = inet_to_str(ip.dst)
        data["UdpSrcP"]         = int(udp.sport)
        data["UdpDstP"]         = int(udp.dport)
        data["UdpUlen"]         = int(udp.ulen)
        data["UdpSum"]          = int(udp.sum)
        data["MAVL_type"]       = mavlink_msg_type
        data["MAVL_len"]        = len(mavlink_data)

        total.append(data)

    f = open("UDP_Report.txt","w")
    f.write(json.dumps(total, indent=4))
    f.close()

def test():
    """Open up a test pcap file and print out the packets"""
    with open('tcpdump.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        print_packets(pcap)

if __name__ == '__main__':
    test()

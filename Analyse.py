from __future__ import print_function
import matplotlib.pyplot as plt
import json
import math

f = open("UDP_Report.txt","r")
data = json.load(f)
f.close()

src_ip      = "192.168.1.18"

def process_list(ar,label="None"):
    try:
        bytes = sum( [x["UdpUlen"] for x in ar] )
    except:
        bytes = 0
    try:
        time = ar[-1]["Time"] - ar[0]["Time"]
    except:
        time = 0
    try:
        rate = float(bytes)/time
    except:
        rate = 0
    print("### %s ###" %(label))
    print("UDP:\t%i\tdatagrams"     %   (len(ar)))
    print("Data:\t%i\tbytes"        %   (int(bytes)))
    print("Time:\t%.2f\ts"         %   (time))
    print("Rate:\t%.2f\tbytes/s"    %   (rate))


def summarise(ar):

    summary_ar = {}

    for item in ar:
        t = item["Time"]
        t = math.floor(t)

        if t not in summary_ar.keys():
            d = {}
            for key in item.keys():
                d[key] = []
            summary_ar[t] = d

        d = summary_ar[t]
        for key in item.keys():
            l = d[key]
            l.append(item[key])
            d[key] = l
        summary_ar[t] = d

    return


sent        = []
received    = []

for item in data:
    if item["IpSrc"] == src_ip:
        sent.append(item)
    if item["IpDst"] == src_ip:
        received.append(item)

process_list(sent,"Sent")
process_list(received,"Received")

#!/bin/bash

sudo tcpdump -n port 14550 -xx -w tcpdump.pcap
python2 PCap_Parser.py
python2 Analyse.py

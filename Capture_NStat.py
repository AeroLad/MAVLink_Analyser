from __future__ import print_function
import subprocess
import threading
import time
import json

global total
total = []

def getNStat():
    global t
    t = threading.Timer(0.2, getNStat)
    t.start()

    data = {"Time": "%.6f" %(time.time())}
    output = subprocess.check_output(["nstat","-az"])
    output = output.split("\n")
    for line in output:
        info = line.split()
        if len(info) < 3:
            continue
        key     = info[0]
        value   = info[1]
        rate    = info[2]
        if "Udp" in key and "Udp6" not in key and "UdpLite" not in key:
            data[key] = {
                            "Value" : value,
                            "Rate"  : rate
                        }

    total.append(data)

getNStat()
print("Exit?")
input = raw_input()
input = input.lower()
if input in ["q","y"]:
    while t.is_alive() == False:
        time.sleep(0.2)
    t.cancel()

    f = open("NStat.txt","w")
    f.write(json.dumps(total,indent=4))
    f.close

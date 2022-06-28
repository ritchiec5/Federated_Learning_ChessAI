
import chess
import chess.engine
import sys 
from telnetlib import Telnet

import requests
IPADDRESS = "172.30.138.120"
res = requests.get("http://{}:5000/".format(IPADDRESS) + 'server/send_global_weights',
                       json="Requesting Global model Data")
print('Received Global Model from Server\n')
# tn = Telnet('localhost', port=8081)
# tn.interact()

# position = "position fen " + "rnbqkbnr/pppp1ppp/8/4p3/8/6PN/PPPPPP1P/RNBQKB1R"
# tn.write(position.encode('ascii') + b"\n")
# tn.write("eval".encode('ascii') + b"\n")
# tn.write("quit".encode('ascii') + b"\n")
# # print(tn.read_all().decode('ascii'))
# info = tn.read_all().decode('ascii')


# info = info.splitlines()
# for line in info:
#     if "Total evaluation" in line: 
#         line = line.replace("Total evaluation: ","")
#         line = line.replace(" (white side)", "")
#         line = float(line) + 1
#         print(line)


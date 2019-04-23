import os

#makes dticts of crytpo adddress and allowed crypto
cryptoaddress = {}
cryptoallowed = {}
file = open("dbs.txt","r")
for line in file:
    a = line.split()
    b = a[0].split(":")
    cryptoaddress[b[0]]=a[1]
    cryptoallowed[b[0]]=a[2]
file.close()

#worker name
workername = "worker1"
file = open("worker.txt","r")
if file.readline().strip():
    workername = file.readline()
file.close()

global minerpath = {"ETH": [os.getcwd()+"\miners\ethash\start.bat","https://api.ethermine.org"], "ZEC": ["miners\equihash\ZecMiner64","https://api-zcash.flypool.org"]}
global process = None
#---------------------------------------------------------
global workername = workername
global cryptoaddress = cryptoaddress
global cryptoallowed = cryptoallowed
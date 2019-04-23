from PyQt5 import QtWidgets, uic
import subprocess
import os
import threading
from time import *
import ethapi.api as api
import demjson
import sys

app = QtWidgets.QApplication([])

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

def runMiner(pot):
        '''
        Dinamično(v podprocesu) zažene minerja (exe), ki je na določeni poti (path).
        Ni potrebe po večih metodah.
        '''
        process = subprocess.Popen(pot, shell=True, stdout=subprocess.PIPE)
        #for line in process.stdout:
        #   print(line)

    def start(args):            #združit izpisovanje in to
        '''
        V currency se shrani trenutno izbrana kriptovaluta.
        V niti se zažene metoda runMiner, kot argument prejme:
        self.minerpath[currency] , kar je slovar v katerem so shranjene kripto kratice
        in v njem poti do programov.
        '''

        minerpath = {"ETH": [os.getcwd()+"\miners\ethash\start.bat","https://api.ethermine.org"], "ZEC": ["miners\equihash\ZecMiner64","https://api-zcash.flypool.org"]}
        thread = threading.Thread(target=runMiner, args=[minerpath[sys.argv[1]][0]])
        thread.start()
        ##self.izpisovanje()


class main_window:
    def __init__(self):
        self.dlg = uic.loadUi("dialog.ui")
        self.dlg.setWindowTitle('Miner by Odisity')
        self.settings = settings()
        self.dlg.cbCurrency.addItems(i for i in cryptoallowed if cryptoallowed[i]=="True")  #to za allow/in not allow bi zbrisal
        self.dlg.btStart.clicked.connect(self.start)
        self.dlg.btSettings.clicked.connect(self.openSettings)
        self.dlg.btStop.clicked.connect(self.stop)
        self.dlg.btStop.setEnabled(False)
        self.minerpath = {"ETH": [os.getcwd()+"\miners\ethash\start.bat","https://api.ethermine.org"], "ZEC": ["miners\equihash\ZecMiner64","https://api-zcash.flypool.org"]}
        self.process = None
        self.dlg.show()

    def izpisovanje(self):
        currency = self.dlg.cbCurrency.currentText() # Kriptovaluta ki je v dropdownu, ETC, ZEC...
        # ustvari novo nit za izpisovanje
        # currency (string) se doda kot argument funkciji izpisiCrypto
        self.izCrypto = threading.Thread(target=self.izpisiCrypto, args=[currency])
        self.izCrypto.start()

    def izpisiCrypto(self, currency):
        '''
        Izpis, ki dela za obe kriptovaluti brez da bi imeli ločeni metodi.
        '''
        try:
            ENDPOINT = self.minerpath[currency][1]
            MINER_ID = cryptoaddress[currency]
            miner = api.Miner(endpoint=ENDPOINT)
            stats = miner.currentstats(miner_id=MINER_ID)
            decoded = demjson.decode(stats)
            unpaid = str(decoded["data"]["unpaid"])
            if len(unpaid) == 15:
                izpis = "0.000" + unpaid[:2]
            if len(unpaid) == 16:
                izpis = "0.00" + unpaid[:3]
            if len(unpaid) == 17:
                izpis = "0.0" + unpaid[:4]
            if len(unpaid) == 18:
                izpis = "0." + unpaid[:5]
            if len(unpaid) == 19:
                izpis = unpaid[:1] + "." + unpaid[4:]
            self.dlg.lb_hash.setText(izpis + " "+currency)
        except:
            self.dlg.lb_hash.setText("0 "+currency)
        sleep(600)
        self.izpisiCrypto(currency)

    def runXMR(self):
        self.process = subprocess.Popen(["miners/monero/xmrig"], stdout=subprocess.PIPE)
        for line in self.process.stdout:
            print(line)

    def runMiner(self, pot):
        '''
        Dinamično(v podprocesu) zažene minerja (exe), ki je na določeni poti (path).
        Ni potrebe po večih metodah.
        '''
        self.process = subprocess.Popen(pot, shell=True, stdout=subprocess.PIPE)
        self.dlg.cbCurrency.setEnabled(False)
        for line in self.process.stdout:
            print(line)

    def start(self):            #združit izpisovanje in to
        '''
        V currency se shrani trenutno izbrana kriptovaluta.
        V niti se zažene metoda runMiner, kot argument prejme:
        self.minerpath[currency] , kar je slovar v katerem so shranjene kripto kratice
        in v njem poti do programov.
        '''
        currency = self.dlg.cbCurrency.currentText()
        self.dlg.lb_izbor.setText("Running " + currency)
        self.thread = threading.Thread(target=self.runMiner, args=[self.minerpath[currency][0]])
        self.thread.start()
        self.dlg.btStart.setEnabled(False)
        self.dlg.btStop.setEnabled(True)
        self.izpisovanje()

    def stop(self):
        '''
        Zaustavi trenutno aktivnega minerja.
        Onemogoči gumb Stop in omogoči gumb Start
        '''
        currency = self.dlg.cbCurrency.currentText()
        if currency in "ETH,ZEC" and self.process is not None:
            self.process.kill()
            self.dlg.cbCurrency.setEnabled(True)
        self.dlg.btStop.setEnabled(False)
        self.dlg.btStart.setEnabled(True)
        self.dlg.lb_izbor.setText("Stopped")

    def openSettings(self):
        #calls class settings
        self.settings.dlgs.show()


class settings:
    def __init__(self):
        self.dlgs = uic.loadUi("settings.ui")
        self.dlgs.setWindowTitle('Settings')
        self.minerpath = {"ETH": "\miners\ethash\start.bat", "ZEC": "miners\equihash\start.bat"}
        self.region = ["EU", "US East", "US West", "ASIA"]
        self.ETHpools = {"EU": "eu1.ethermine.org:4444", "US East": "us1.ethermine.org:4444",
                         "US West": "us2.ethermine.org:4444", "ASIA": "asia1.ethermine.org:4444"}
        self.dlgs.cbRegion.addItems(i for i in self.region)
        #saved values
        self.dlgs.leETH.setText(cryptoaddress["ETH"])
        self.dlgs.leZEC.setText(cryptoaddress["ZEC"])
        if cryptoallowed["ETH"]=="True":
            self.dlgs.chETH.setChecked(True)
        if cryptoallowed["ZEC"]=="True":
            self.dlgs.chZEC.setChecked(True)
        self.dlgs.btSave.clicked.connect(self.save)
        #self.dlgs.show()

    def zapisovanje(self):
        chosenRegion = self.dlgs.cbRegion.currentText()
        ethadr = str(self.dlgs.leETH.text())
        zecadr = str(self.dlgs.leZEC.text())

        #ETH
        file2 = open(self.minerpath["ETH"], "r")
        for line in file2:
            b = line.split(" ")
            c = b[4]
        c = c.split(".")
        # work = c[1]   v settingsih jim bomo ponudli še ime workerja če želijo
        nova = ethadr + "." + c[1]
        string = b[0] + " " + b[1] + " " + b[2] + " " + b[3] + " " + nova + " " + " " + b[5] + " " + b[6]
        file2.close()
        file2 = open("miners/ethash/start.bat", "w")
        file2.write(string)
        file2.close()

    def save(self):
        #ETH
        ethadr = str(self.dlgs.leETH.text())
        zecadr = str(self.dlgs.leZEC.text())
        if self.dlgs.chETH.isChecked():
            cheth = "True"
        else:
            cheth = "False"
        #ZEC
        if self.dlgs.chZEC.isChecked():
            chzec = "True"
        else:
            chzec = "False"
        #empty address
        if ethadr=="":
            ethadr = "empty"
        if zecadr=="":
            zecadr = "empty"
        #save to file
        file = open("dbs.txt","w")
        file.write("ETH: "+ethadr+" "+cheth)
        file.write("\n")
        file.write("ZEC: "+zecadr+" "+chzec)
        file.close()
        self.dlgs.hide()
        #os.execl(sys.executable, sys.executable, *sys.argv)

miner = main_window()
app.exec()
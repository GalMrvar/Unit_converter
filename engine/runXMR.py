def runXMR(self):
        self.process = subprocess.Popen(["miners/monero/xmrig"], stdout=subprocess.PIPE)
        for line in self.process.stdout:
            print(line)
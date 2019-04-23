from time import *
import ethapi.api as api
import demjson
import main
 
    def izpisiCrypto(self, currency):
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
            current = izpis + " " + currency
        except:
            current = "0 " + currency
        sleep(600)
        #nekam izpise treba še popravit
        print(current)
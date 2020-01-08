from pymetasploit3.msfrpc import MsfRpcClient
from pymetasploit3.msfconsole import MsfRpcConsole
import time


class Metasploit:

    def __init__(self, password, user):
        print("[INFOS] Authentification to Metasploit (msfrpcd) ...")
        self._client = MsfRpcClient(password=password, port=55556)
        self._client.login(user=user, password=password)

        if self._client.authenticated:
            print("[SUCESS] Authentification MSFRPC SUCESS")
        else:
            print("[ERROR] Authentification ERROR !")

        self._console = MsfRpcConsole(self._client, cb=self.read_console)
        self.client_Isbusy = False
        self._console_read = list()
        self._console_data = None

    def read_console(self, console_data):
        self.client_Isbusy = console_data['busy']
        # print("Console State : " + str(self._console_busy))

        if '[+]' in console_data['data']:
            sigdata = console_data['data'].rstrip().split('\n')

            for line in sigdata:
                if '[+]' in line:
                    self._console_read.append(line)
        # self._console_data = console_data
        # print("\n\n")
        # print(self._console_data)
        # print("\n\n")
        # print("\n\n")
        print(console_data['data'])

    def send_cmd(self, cmd):
        if self._client.authenticated and not self.client_Isbusy:
            self._console.execute(cmd)
            time.sleep(5)
        elif self.client_Isbusy:
            print("[WAITING] Client was busy !")
            while self.client_Isbusy:
                time.sleep(5)

            print("[INFOS] Client Available now !")
            self._console.execute(cmd)
            time.sleep(5)
        else:
            print("[ERROR] Client Was Not Authentificated !")

